import pandas as pd
import numpy as np
import streamlit as st
import requests
import json
from requests import get
from matplotlib import pyplot as plt
from datetime import datetime
from config import *
import plotly.express as px
from web3 import Web3
from config import *
from opensea import OpenseaAPI
api = OpenseaAPI(apikey=API_KEY_OS)




 	###################  
    ###  Funtions   ###
    ###################

eth_value = 10 ** 18

web3_connection = Web3(Web3.HTTPProvider(node_provider))


# PLOT ANY GIVEN ADDRESS BALANCE
# ----------------------------------------------------------------------------------------------- 
def plot_any_wallet(address):
	# for normal tx:
	get_normal_tx_url = make_api_url('account', 'txlist', address, startblock=0, endblock=99999999, page=1, offset=10000, sort='asc')
	response = get(get_normal_tx_url)
	data = response.json()['result']

	# for internal tx:
	get_internal_tx_url = make_api_url('account', 'txlist', address, startblock=0, endblock=99999999, page=1, offset=10000, sort='asc')
	response2 = get(get_internal_tx_url)
	data2 = response2.json()['result']

	data.extend(data2)
	data.sort(key=lambda x: int(x['timeStamp']))
	

	current_balance = 0
	balances = []
	times = []
	
	for tx in data:
		to = tx['to']
		from_addr = tx['from']
		value = int(tx['value']) / eth_value
		if 'gasPrice' in tx:
			gas = int(tx['gasUsed']) * int(tx['gasPrice']) /eth_value
		else:
			gas = int(tx['gasUsed']) /eth_value

		time = datetime.fromtimestamp(int(tx['timeStamp']))
		money_in = to.lower() == operations_wallet.lower()
		
		if money_in:
			current_balance += value
		else: 
			current_balance -= value + gas

		balances.append(current_balance)
		times.append(time)
	sns.lineplot(x=times, y=balances)
	plt.show()
	# ----------------------------------------------------------------------------------------------- 



# GET the API URL automatically
# ----------------------------------------------------------------------------------------------- 
def make_api_url(module, action, address, **kwargs):
    url = BASE_URL + f"?module={module}&action={action}&address={address}&apikey={API_KEY}"

    for key, value in kwargs.items():
        url += f"&{key}={value}"

    return url
# ----------------------------------------------------------------------------------------------- 



# GET ALL TRANSACTION FOR A GIVEN ADDRESS
# ----------------------------------------------------------------------------------------------- 
def get_transactions(address):
    # for normal tx:
    get_normal_tx_url = make_api_url('account', 'txlist', address, startblock=0, endblock=99999999, page=1, offset=10000, sort='asc')
    response = get(get_normal_tx_url)
    data = response.json()['result']

    # for internal tx:
    get_internal_tx_url = make_api_url('account', 'txlist', address, startblock=0, endblock=99999999, page=1, offset=10000, sort='asc')
    response2 = get(get_internal_tx_url)
    data2 = response2.json()['result']

    for tx in data:
        to = tx['to']
        from_addr = tx['from']
        value = int(tx['value']) / eth_value
        gas = tx['gasUsed']
        time = datetime.fromtimestamp(int(tx['timeStamp']))
        print('-----------')
        print('to:', to)
        print('from:', from_addr)
        print('value:', value)
        print('gas used:', gas)
        print('Time:', time)
# ----------------------------------------------------------------------------------------------- 




# OBTAIN CURRENT ADDRESS BALANCE
# ----------------------------------------------------------------------------------------------- 
def get_account_balance(address):
    balance_url = make_api_url("account", "balance", address, tag="latest")
    response = get(balance_url)
    data = response.json()

    value = int(data["result"]) / eth_value
    print(value)
# ----------------------------------------------------------------------------------------------- 




# OBTAINS COMMUNITY WALLET BALANCE OVER TIME
# ----------------------------------------------------------------------------------------------- 
def plot_community_wallet(community_wallet):
    # for normal tx:
    get_normal_tx_url = make_api_url('account', 'txlist', community_wallet, startblock=0, endblock=99999999, page=1, offset=10000, sort='asc')
    response = get(get_normal_tx_url)
    data = response.json()['result']

    # for internal tx:
    get_internal_tx_url = make_api_url('account', 'txlist', community_wallet, startblock=0, endblock=99999999, page=1, offset=10000, sort='asc')
    response2 = get(get_internal_tx_url)
    data2 = response2.json()['result']

    data.extend(data2)
    data.sort(key=lambda x: int(x['timeStamp']))
    

    current_balance = 0
    balances = []
    times = []
    
    for tx in data:
        to = tx['to']
        from_addr = tx['from']
        value = int(tx['value']) / eth_value
        if 'gasPrice' in tx:
            gas = int(tx['gasUsed']) * int(tx['gasPrice']) /eth_value
        else:
            gas = int(tx['gasUsed']) /eth_value

        time = datetime.fromtimestamp(int(tx['timeStamp']))
        money_in = to.lower() == community_wallet.lower()
        
        if money_in:
            current_balance += value
        else: 
            current_balance -= value + gas

        balances.append(current_balance)
        times.append(time)

    plt.plot(times, balances, color='b', linewidth='0.8')
    plt.xlabel('Date')
    plt.ylabel('Account Balance')
    plt.title('inBetweeners Community Wallet Account Balance')
    plt.show()
# ----------------------------------------------------------------------------------------------- #




# PLOTS OPERATIONS WALLET BALANCE OVER TIME
# ----------------------------------------------------------------------------------------------- #
def plot_operations_wallet():
    # for normal tx:
    get_normal_tx_url = make_api_url('account', 'txlist', operations_wallet, startblock=0, endblock=99999999, page=1, offset=10000, sort='asc')
    response = get(get_normal_tx_url)
    data = response.json()['result']

    # for internal tx:
    get_internal_tx_url = make_api_url('account', 'txlist', operations_wallet, startblock=0, endblock=99999999, page=1, offset=10000, sort='asc')
    response2 = get(get_internal_tx_url)
    data2 = response2.json()['result']

    data.extend(data2)
    data.sort(key=lambda x: int(x['timeStamp']))
    

    current_balance = 0
    balances = []
    times = []
    balances_df = pd.DataFrame({'balances':balances, 'times':times})
    
    for tx in data:
        to = tx['to']
        from_addr = tx['from']
        value = int(tx['value']) / eth_value
        if 'gasPrice' in tx:
            gas = int(tx['gasUsed']) * int(tx['gasPrice']) /eth_value
        else:
            gas = int(tx['gasUsed']) /eth_value

        time = datetime.fromtimestamp(int(tx['timeStamp']))
        money_in = to.lower() == operations_wallet.lower()
        
        if money_in:
            current_balance += value
        else: 
            current_balance -= value + gas

        balances.append(current_balance)
        times.append(time)

    fig = px.line(balances_df, x=times, y=balances, title='Operations Wallet: Balance over time', markers=True,
        labels={
                     "x": "Date",
                     "y": "Balance",
                 },)
    fig.update_traces(line_color='#FFA500')
    return fig
# ----------------------------------------------------------------------------------------------- #





# PLOTS THE COMMUNITY WALLET BALANCE
# ----------------------------------------------------------------------------------------------- #
def plot_community_wallet():
    # for normal tx:
    get_normal_tx_url = make_api_url('account', 'txlist', community_wallet, startblock=0, endblock=99999999, page=1, offset=10000, sort='asc')
    response = get(get_normal_tx_url)
    data = response.json()['result']

    # for internal tx:
    get_internal_tx_url = make_api_url('account', 'txlist', community_wallet, startblock=0, endblock=99999999, page=1, offset=10000, sort='asc')
    response2 = get(get_internal_tx_url)
    data2 = response2.json()['result']

    data.extend(data2)
    data.sort(key=lambda x: int(x['timeStamp']))
    

    current_balance = 0
    balances = []
    times = []
    balances_df = pd.DataFrame({'balances':balances, 'times':times})
    
    for tx in data:
        to = tx['to']
        from_addr = tx['from']
        value = int(tx['value']) / eth_value
        if 'gasPrice' in tx:
            gas = int(tx['gasUsed']) * int(tx['gasPrice']) /eth_value
        else:
            gas = int(tx['gasUsed']) /eth_value

        time = datetime.fromtimestamp(int(tx['timeStamp']))
        money_in = to.lower() == community_wallet.lower()
        
        if money_in:
            current_balance += value
        else: 
            current_balance -= value + gas

        balances.append(current_balance)
        times.append(time)

    fig = px.line(balances_df, x=times, y=balances, title='Community Wallet: Balance over time', markers=True,
        labels={
                     "x": "Date",
                     "y": "Balance",
                 },)
    fig.update_traces(line_color='#8A2BE2')
    return fig
# ----------------------------------------------------------------------------------------------- #

# Connection

def connection():
    print(web3_connection.isConnected())

# Get token balance from a given address

def token_balance_ERC20(ERC20_address):
    ERC20_address = Web3.toChecksumAddress(ERC20_address)
    contract = web3_connection.eth.contract(address=contract_address, abi=contract_abi) # creates a contract object
    balance_token = contract.functions.balanceOf(ERC20_address).call()
    #print(balance_token)
    return(balance_token)

# OpenSea API
# get NFT(token) info
def get_token_image(token_id):
    result = api.asset(asset_contract_address=contract_address, token_id=token_id)
    #print("NFT name: ", result["name"])
    #print("Image URL: ", result["image_url"])

    return(result["image_url"])

# get amount of owners
def num_owners():
    stats = api.collection_stats(collection_slug="inbetweeners")
    return(stats['stats']['num_owners'])

# get floor price
def get_floor_price():
    fp = api.collection_stats(collection_slug="inbetweeners")
    return(fp['stats']['floor_price'])

# get volume
def get_total_volume():
    volume = api.collection_stats(collection_slug="inbetweeners")
    return(volume['stats']['floor_price'])