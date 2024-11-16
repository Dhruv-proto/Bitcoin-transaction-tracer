import requests
import csv
import pandas as pd
import networkx as nx
from datetime import datetime
import os

# Function to fetch transaction data from blockchain.info
def fetch_transaction_data(txid):
    url = f"https://blockchain.info/rawtx/{txid}?format=json"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Function to fetch all transactions linked to a given address
def fetch_address_data(address):
    url = f"https://blockchain.info/rawaddr/{address}?format=json"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Function to convert Unix timestamp to human-readable format
def convert_timestamp(timestamp):
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

# Function to parse transaction data and extract details
def parse_transaction_data(tx_data):
    parsed_data = []
    for tx in tx_data:
        txid = tx['hash']
        time = convert_timestamp(tx['time'])
        inputs = tx['inputs']
        outputs = tx['out']

        for inp in inputs:
            source = inp['prev_out'].get('addr', 'unknown')
            for out in outputs:
                recipient = out.get('addr', 'unknown')
                value = out['value'] / 100000000  # Convert Satoshis to BTC
                parsed_data.append({
                    'Transaction ID': txid,
                    'Source': source,
                    'Received By': recipient,
                    'Value (BTC)': value,
                    'Time': time
                })
    return parsed_data

# Function to display parsed data in tabular format
def display_transaction_data(parsed_data):
    df = pd.DataFrame(parsed_data)
    print("\\nTransaction Data:")
    print(df)

# Function to save parsed transaction data to CSV
def save_to_csv(parsed_data, filename, folder_path):
    filepath = os.path.join(folder_path, filename)
    df = pd.DataFrame(parsed_data)
    df.to_csv(filepath, index=False)
    print(f"Transaction data saved to {filepath}")

# Function to prepare raw data for graph representation
# Function to prepare raw data for graph representation
def prepare_graph_data(transactions):
    G = nx.DiGraph()

    for tx in transactions:
        txid = tx['hash']
        inputs = tx['inputs']
        outputs = tx['out']

        # Add edges from inputs to outputs with the transaction value
        for inp in inputs:
            source = inp['prev_out'].get('addr', 'unknown')
            for out in outputs:
                target = out.get('addr', 'unknown')
                value = out['value'] / 100000000  # Convert Satoshis to BTC
                if source != 'unknown' and target != 'unknown':
                    G.add_edge(source, target, txid=txid, value=value)

    return G

# Function to export graph data for external software like GraphXR
def export_graph_data(graph, filename,folder_path):
    filepath = os.path.join(folder_path, filename)
    edges_data = [
        {"source": edge[0], "target": edge[1], "value": edge[2]['value'], "transaction_id": edge[2]['txid']}
        for edge in graph.edges(data=True)
    ]
    edges_df = pd.DataFrame(edges_data)
    edges_df.to_csv(filepath, index=False)
    print(f"Graph data saved to {filepath}")



