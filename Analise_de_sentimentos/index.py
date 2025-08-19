import tweepy
import pandas as pd
import re
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import seaborn as sns

## inicio do codigo 



try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except nltk.downloader.DownloadError:
    nltk.download('vader_lexicon')


bearer_token = "API_SEAAAAAAAAAAAAAAAAAAAAAMVr3gEAAAAAK5HqS7c%2Bu1H0rf7XRNo0WsehOvc%3DTNYfpdDA1o0exYmzMxkcOS7Aofq3BNJBCSLAYhCo50N3vpEY9bNTIMENTOS"
client = tweepy.Client(bearer_token)

def coletar_tweets(termo_busca, num_tweets):

    print(f"Coletando {num_tweets} tweets para o termo '{termo_busca}'...")
    response = client.search_recent_tweets(query=termo_busca, max_results=num_tweets)
    
    data = []
    if response.data:
        for tweet in response.data:
            data.append(tweet.text)
    
    df = pd.DataFrame(data, columns=['tweet_text'])
    return df

def preprocessar_texto(texto):


    texto = re.sub(r'https?://\S+|www\.\S+', '', texto)

    texto = re.sub(r'@[A-Za-z0-9_]+', '', texto)

    texto = re.sub(r'#', '', texto)

    texto = re.sub(r'[^a-zA-Z\s]', '', texto)

    texto = texto.lower()
    return texto

def analisar_sentimento(texto):

    analisador = SentimentIntensityAnalyzer()
    pontuacao_sentimento = analisador.polarity_scores(texto)
    
    if pontuacao_sentimento['compound'] >= 0.05:
        return 'Positivo'
    elif pontuacao_sentimento['compound'] <= -0.05:
        return 'Negativo'
    else:
        return 'Neutro'

def visualizar_resultados(df_sentimento):

    plt.style.use('seaborn-v0_8-darkgrid')
    
    contagem_sentimento = df_sentimento['sentimento'].value_counts()
    
    plt.figure(figsize=(8, 6))
    ax = sns.barplot(x=contagem_sentimento.index, y=contagem_sentimento.values, palette=['#4CAF50', '#FF5733', '#808080'])
    
    for p in ax.patches:
        ax.annotate(f'{p.get_height()}', (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', fontsize=12, color='black', xytext=(0, 5),
                    textcoords='offset points')
                    
    plt.title('Distribuição de Sentimento', fontsize=16)
    plt.xlabel('Sentimento', fontsize=12)
    plt.ylabel('Contagem de Tweets', fontsize=12)
    plt.show()


if __name__ == "__main__":

    termo = "Felca" 
    num_tweets = 100
    df_tweets = coletar_tweets(termo, num_tweets)
    
    if not df_tweets.empty:
        df_tweets['texto_limpo'] = df_tweets['tweet_text'].apply(preprocessar_texto)
        
        df_tweets['sentimento'] = df_tweets['texto_limpo'].apply(analisar_sentimento)
        
        visualizar_resultados(df_tweets)
        
        print("\n--- Tabela de Resultados ---")
        print(df_tweets[['tweet_text', 'sentimento']].head(10))
    else:
        print("Nenhum tweet foi encontrado. Verifique seu token e o termo de busca.")
