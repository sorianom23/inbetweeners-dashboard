# Python libraries
import token
#from turtle import width
import pandas as pd
import streamlit as st
#import seaborn as sns
import requests
import json
from requests import get
from matplotlib import pyplot as plt
from datetime import datetime
from config import *
import plotly.express as px

from functions import * # let's try this now

# images
image1 = '/Users/mariasoriano/Documents/data/inbetweeners/src/images/bear1.png'
image2 = '/Users/mariasoriano/Documents/data/inbetweeners/src/images/bear2.png'
image3 = '/Users/mariasoriano/Documents/data/inbetweeners/src/images/bear3.png'
image4 = '/Users/mariasoriano/Documents/data/inbetweeners/src/images/bear4.png'
image5 = '/Users/mariasoriano/Documents/data/inbetweeners/src/images/bear5.png'
image6 = '/Users/mariasoriano/Documents/data/inbetweeners/src/images/banner.png'

# User module files
#from streamlit_lottie import st_lottie
#from streamlit_option_menu import option_menu

# Connection to Web3
web3_connection = Web3(Web3.HTTPProvider(node_provider))


eth_value = 10 ** 18

operations_wallet='0x6d59efcb15362840ae0469547ff5b7bb794bb48d'
community_wallet = '0x42907c1193762f567345de09560250c63fdae076'



  
    #############  
    # Main page #
    #############   

st.set_page_config(page_title="Etherscan project", page_icon=":bear:", layout="wide")

c1 = st.container()
with c1:
    col1, col2, col3 = st.columns(3)
    with col2:
        st.header('🧸 inBetweeners info 🧸')
        st.image(image6, width=400)
st.markdown("""---""")

c2 = st.container()
with c2:
    col1, col2, col3 = st.columns(3)
    with col1:
        #sidebar = st.sidebar.selectbox('Display founds from:', ('Community Wallet', 'Operations Wallet'))
        option = st.selectbox(
            'Select wallet:',
            ('Community Wallet', 'Operations Wallet'))

        if option == 'Community Wallet':
            st.plotly_chart(plot_community_wallet())

        if option == 'Operations Wallet':
            st.plotly_chart(plot_operations_wallet())


#c2 = st.container()
#with c2:
#    col1, col2, col3 = st.columns(3)
#    with col1:
#        bears = st.slider('How many bears are you holding?', 0, 100, 25)
#        st.write("I'm holding ", bears, 'bears 🧸')

#c3 = st.container()
#with c3:
    #col1, col2, col3 = st.columns(3)
    with col3:
        title = st.text_input('Search a 🧸 by ID', '')
        search_button = st.button('Show image')

        if search_button:
            token_image = get_token_image(title)
            st.image(token_image, width=150)

    #with col2:
        title = st.text_input('Enter an ETH address to see how many bears is holding', '')
        search_button = st.button('Search')

        if search_button:
            token_balance = token_balance_ERC20(title)
            st.write('Holding ', token_balance, 'bears')
st.markdown("""---""")

c3 = st.container()
with c3:
    col1, col2, col3, col4, col5 = st.columns(5)
    col2.metric(label='Floor price', value=get_floor_price())
    col3.metric(label='Total volume', value=get_total_volume())
    col4.metric(label='Number of owners', value=num_owners())
st.markdown("""---""")

c4 = st.container()
with c4:
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.image(image2, caption = '1323')
    with col2:
        st.image(image5, caption = '1742')
    with col3:
        st.image(image3, caption = '1237')
    with col4:
        st.image(image4, caption = '1498')
    with col5:
        st.image(image1, caption = '3842')
st.markdown("""---""")

c5 = st.container()
with c5:
    st.write('If you want to know more about this NFT collection, please check out the official website: https://www.inbetweeners.io/')
