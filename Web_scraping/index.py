import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import matplotlib.pyplot as plt
import seaborn as sns

def raspar_dados_imoveis(url):

    print(f"Raspando dados da URL: {url}...")
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 OPR/77.0.4054.277',
            'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status() 
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        dados_imoveis = []
        
        cards_imoveis = soup.find_all('article', class_='search-new-layout ng-star-inserted')
        
        if not cards_imoveis:
            print("Nenhum 'card' de imóvel encontrado. Verifique a classe HTML usada.")
            return pd.DataFrame() # Retorna um DataFrame vazio se nada for encontrado

        print(f"Encontrados {len(cards_imoveis)} imóveis. Extraindo dados...")

        for card in cards_imoveis:

            preco_tag = card.find('p', class_='price')
            preco = preco_tag.get_text(strip=True) if preco_tag else None
            
            atributos_ul = card.find('ul', class_='attributes ng-star-inserted')
            area = None
            quartos = None
            
            if atributos_ul:
                for li in atributos_ul.find_all('li'):
                    li_text = li.get_text(strip=True)
                    if 'm²' in li_text:
                        area = li_text
                    elif 'quartos' in li_text:
                        quartos = li_text

            localizacao_tag = card.find('p', class_='location')
            localizacao = localizacao_tag.get_text(strip=True) if localizacao_tag else None
            
            dados_imoveis.append({
                'preco_bruto': preco,
                'area_bruta': area,
                'quartos_brutos': quartos,
                'localizacao': localizacao
            })
            
    except requests.exceptions.RequestException as e:
        print(f"Erro ao fazer a requisição HTTP: {e}")
        return pd.DataFrame()
        
    return pd.DataFrame(dados_imoveis)

def limpar_dados(df):
    
    if df.empty:
        print("DataFrame vazio. Não há dados para limpar.")
        return df
        
    print("Iniciando a limpeza dos dados...")
    df_limpo = df.copy()

    df_limpo['preco'] = df_limpo['preco_bruto'].str.replace(r'[R$.\s/mês]', '', regex=True).str.replace(',', '.').astype(float)

    df_limpo['area_m2'] = df_limpo['area_bruta'].str.replace(r'm²', '', regex=False).str.strip().astype(float)
    
    df_limpo['quartos'] = df_limpo['quartos_brutos'].str.extract(r'(\d+)', expand=False).astype(float)
    

    df_limpo = df_limpo.drop(['preco_bruto', 'area_bruta', 'quartos_brutos'], axis=1)
    

    df_limpo = df_limpo.dropna()
    
    print("Limpeza de dados concluída!")
    return df_limpo

def visualizar_dados(df):
    if df.empty:
        print("DataFrame vazio. Não há dados para visualizar.")
        return
        
    print("Criando visualizações...")
    sns.set_style("darkgrid")
    

    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='area_m2', y='preco', data=df)
    plt.title('Preço vs. Área (m²)', fontsize=16)
    plt.xlabel('Área em m²', fontsize=12)
    plt.ylabel('Preço (R$)', fontsize=12)
    plt.show()


if __name__ == "__main__":
    url_alvo = "https://www.lopes.com.br/busca/venda/br/sp/sao-paulo?estagio=real_estate&estagio=real_estate_parent&placeId=ChIJna3KP2VZzpQRPJRhSWh78go&origem=home"
    

    df_bruto = raspar_dados_imoveis(url_alvo)
    

    df_final = limpar_dados(df_bruto)
    
    if not df_final.empty:

        print("\n--- Estatísticas Descritivas dos Dados Limpos ---")
        print(df_final.describe())
        
        visualizar_dados(df_final)
        
        print("\n--- Dados Limpos (Primeiras 5 Linhas) ---")
        print(df_final.head())
    else:
        print("O script não conseguiu coletar ou limpar os dados com sucesso.")
