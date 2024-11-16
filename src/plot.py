import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

def load_graph_from_csv(file_path):
    """
    Load a graph from a CSV file with columns: source, target, value, transaction_id.
    """
    # Read the CSV file
    df = pd.read_csv(file_path)
    
    # Create a directed graph
    G = nx.DiGraph()
    
    # Add edges to the graph with attributes
    for _, row in df.iterrows():
        G.add_edge(row['source'], row['target'], value=row['value'], transaction_id=row['transaction_id'])
    
    return G

def plot_transaction_graph(G):
    """
    Plot the Bitcoin transaction graph using networkx and matplotlib.
    """
    plt.figure(figsize=(12, 8))
    
    # Create a layout for the graph
    pos = nx.spring_layout(G, seed=42)  # Fixed seed for consistent layout

    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_size=700, node_color='lightblue')

    # Draw edges
    nx.draw_networkx_edges(G, pos, edgelist=G.edges, arrowstyle='-|>', arrowsize=15, edge_color='gray')

    # Draw labels for nodes
    nx.draw_networkx_labels(G, pos, font_size=10, font_color='black')

    # Annotate edges with transaction values
    edge_labels = { (u, v): f"{d['value']} BTC" for u, v, d in G.edges(data=True) }
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8, label_pos=0.5)

    # Title and display
    plt.title("Bitcoin Transaction Network", fontsize=16)
    plt.axis('off')
    plt.show()


