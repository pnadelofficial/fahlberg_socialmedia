from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st
import time
from util import *

st.title('Twitter Comments Scraper')
st.write("Input the URL to a Tweet below and wait a couple minutes. Once complete you'll be able to donwload the comments as a CSV and explore some statistics.")

chrome_options = Options()
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
chrome_options.add_argument(f'user-agent={user_agent}')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument("--headless")

@st.cache_resource
def get_driver():
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

wd = get_driver()

url = st.text_input('Use any twitter link')
if url !='':
    wd.get(url)

    tweets = []
    result = False
    old_height = wd.execute_script("return document.body.scrollHeight")
    all_tweets = wd.find_elements(By.XPATH, '//div[@data-testid]//article[@data-testid="tweet"]')

    with st.spinner('Querying Twitter. This might take some time. Please wait...'):

        while result == False:
            
            for item in all_tweets[1:]: # skip tweet already scrapped
                soup = BeautifulSoup(item.get_attribute('outerHTML'))
                try:
                    date = soup.time['datetime']
                except:
                    date = '[empty]'

                try:
                    text = item.find_element(By.XPATH, './/div[@data-testid="tweetText"]').text
                    if len(soup.find_all('img')) > 1:
                        for e in soup.find_all('img')[1:]:
                            text += e['alt']
                except:
                    text = '[empty]'

                try:
                    acc = [a['href'] for a in soup.find_all('a')][0]
                except:
                    acc = '[empty]'

                if date != '[empty]': # ads...
                    tweets.append([date, acc, text])
            
            #scroll down the page
            wd.execute_script("window.scrollTo(0,document.body.scrollHeight)")

            time.sleep(2)

            new_height = wd.execute_script("return document.body.scrollHeight")

            if new_height == old_height:
                result = True
            old_height = new_height

            #update all_tweets to keep loop
            all_tweets = wd.find_elements(By.XPATH, '//div[@data-testid]//article[@data-testid="tweet"]')

    st.success('Successfully scraped comments from this tweet!')
    
    df = pd.DataFrame(tweets).rename(columns={0:'date', 1:'acc_name', 2:'text'})
    df['date'] = pd.to_datetime(df['date'])
    csv = convert_df(df)

    st.download_button(
    "Download Comments Here",
    csv,
    f"tweet_{url.split('/')[-1]}_comments.csv",
    "text/csv",
    key='download-csv'
    )

    with st.expander("See some statistics"):
        st.pyplot(df.groupby(pd.Grouper(key='date', freq='H')).count()['text'].plot(kind='bar', title='Frequency of Tweets over time').figure)
        st.divider()
        freq = count_words(df, relative=True)
        freq = pd.DataFrame(freq).rename(columns={0:'word', 1:'relative_freq'})
        st.pyplot(freq[:20].plot(x='word', y='relative_freq', kind='barh', title='Top 20 words by relative frequency').figure)

st.markdown('<small>This tool is for educational purposes ONLY!</small>', unsafe_allow_html=True)
st.markdown('<small>Assembled by Peter Nadel | TTS Research Technology</small>', unsafe_allow_html=True)        
