import pandas as pd
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import sys
import os

API_KEY = "f9efa3fddeab4e2f0171840b7ec27746" ## usado para teste, não funciona!!! gere um novo no site tmdb

def imprimir_barra_progresso(iteracao, total, prefixo='', sufixo='', comprimento=50, preenchimento='█'):
    percentual = ("{0:.1f}").format(100 * (iteracao / float(total)))
    barras_preenchidas = int(comprimento * iteracao // total)
    barra = preenchimento * barras_preenchidas + '-' * (comprimento - barras_preenchidas)
    
    sys.stdout.write(f'\r{prefixo} |{barra}| {percentual}% {sufixo}')
    sys.stdout.flush()

def obter_dados_filmes(api_key, num_paginas=100):
    print("Coletando dados de filmes da API do TMDb...")
    base_url = "https://api.themoviedb.org/3/movie/popular"
    dados_totais = []

    try:
        for pagina in range(1, num_paginas + 1):
            params = {
                'api_key': api_key,
                'language': 'pt-BR',
                'page': pagina
            }
            response = requests.get(base_url, params=params)
            response.raise_for_status() 
            dados = response.json().get('results', [])
            dados_totais.extend(dados)
            
            imprimir_barra_progresso(pagina, num_paginas, prefixo='Progresso:', sufixo=f'Pagina {pagina}/{num_paginas}')

    except requests.exceptions.RequestException as e:
        print("\n", file=sys.stderr) 
        print(f"Erro ao coletar dados da API do TMDb: {e}", file=sys.stderr)
        return pd.DataFrame() 

    if not dados_totais:
        print("\n", file=sys.stderr)
        print("Nenhum dado de filme encontrado. Verifique sua chave de API.", file=sys.stderr)
        return pd.DataFrame()

    df = pd.DataFrame(dados_totais)

    colunas_relevantes = ['title', 'overview', 'genre_ids']
    df_selecionado = df[colunas_relevantes]
    return df_selecionado

def criar_vetorizador_tfidf(df):
    print("\nCriando matriz TF-IDF...")
    tfidf = TfidfVectorizer(stop_words='english')
    df['overview'] = df['overview'].fillna('')
    tfidf_matriz = tfidf.fit_transform(df['overview'])
    return tfidf_matriz, tfidf

def calcular_similaridade_cosseno(tfidf_matriz):
    print("Calculando similaridade de cosseno...")
    similaridade_cosseno = cosine_similarity(tfidf_matriz, tfidf_matriz)
    return similaridade_cosseno

def obter_recomendacoes(titulo_filme, df, similaridade_matriz):
    if titulo_filme not in df['title'].values:
        print(f"Filme '{titulo_filme}' nao encontrado na base de dados.", file=sys.stderr)
        return []

    indice_filme = df[df['title'] == titulo_filme].index[0]
    
    pontuacoes_similares = list(enumerate(similaridade_matriz[indice_filme]))
    
    pontuacoes_similares = sorted(pontuacoes_similares, key=lambda x: x[1], reverse=True)
    
    pontuacoes_filmes_similares = pontuacoes_similares[1:11]
    
    indices_filmes = [i[0] for i in pontuacoes_filmes_similares]
    
    return df['title'].iloc[indices_filmes].tolist()

if __name__ == "__main__":
    if API_KEY == "":
        print("deu erro na api (chave)", file=sys.stderr)
    else:

        df_filmes = obter_dados_filmes(API_KEY)
        
        if not df_filmes.empty:
            print("\nColeta de dados concluida!")

            tfidf_matriz, tfidf_vetorizador = criar_vetorizador_tfidf(df_filmes)
            
            matriz_similaridade = calcular_similaridade_cosseno(tfidf_matriz)
            
            filme_referencia = "A Freira" 
            recomendacoes = obter_recomendacoes(filme_referencia, df_filmes, matriz_similaridade)
            
            if recomendacoes:
                print(f"\n--- Top 10 filmes recomendados para '{filme_referencia}' ---")
                for i, filme in enumerate(recomendacoes, 1):
                    print(f"{i}. {filme}")
