import plot as pt
import track as tk
import os
def main():
    ascii_art=""" 
.______    __  .___________..______          ___       ______  __  ___ 
|   _  \\  |  | |           ||   _  \\        /   \\     /      ||  |/  / 
|  |_)  | |  | `---|  |----`|  |_)  |      /  ^  \\   |  ,----'|  '  /  
|   _  <  |  |     |  |     |      /      /  /_\\  \\  |  |     |    <   
|  |_)  | |  |     |  |     |  |\\  \\----./  _____  \\ |  `----.|  .  \\  
|______/  |__|     |__|     | _| `._____/__/     \\__\\ \\______||__|\\__\\ 
                                                                       
"""
    print(ascii_art)
    i=0
    while i==0:
        print('''1) Trace a transaction or wallet address
2) Visualize findings
3) Exit''')
        option=int(input("Enter your choice:"))
        if option==1:

            user_input = input("Enter wallet address or transaction ID: ")
            current_dir = os.path.dirname(os.path.abspath(__file__))
            saved_data_folder = os.path.join(current_dir, "saved_data")
            if len(user_input) == 64:  # Assuming it's a transaction ID
                tx_data = tk.fetch_transaction_data(user_input)
                if tx_data:

                    parsed_data = tk.parse_transaction_data([tx_data])
                    tk.display_transaction_data(parsed_data)
                    tk.save_to_csv(parsed_data, "transaction_data.csv", saved_data_folder)
                    graph = tk.prepare_graph_data([tx_data])
                    tk.export_graph_data(graph, "graph_data.csv", saved_data_folder)
                else:
                    print("Transaction not found.")
            else:  # Assuming it's a wallet address
                address_data = tk.fetch_address_data(user_input)
                if address_data:
                    parsed_data = tk.parse_transaction_data(address_data['txs'])
                    tk.display_transaction_data(parsed_data)
                    tk.save_to_csv(parsed_data, "transactions.csv", saved_data_folder)
                    graph = tk.prepare_graph_data(address_data['txs'])
                    tk.export_graph_data(graph, "graph_data.csv", saved_data_folder)
                else:
                    print("Address not found.")
            
        
        elif option==2:
                # Get CSV file path from the user
                file_path = "saved_data\\graph_data.csv"

                try:
                    # Load the graph from the CSV file
                    G = pt.load_graph_from_csv(file_path)

                    # Plot the transaction graph
                    pt.plot_transaction_graph(G)

                except Exception as e:
                    print(f"Error: {e}")
            

        else:
            print("Thank you!")
            i=1

if __name__ == "__main__":
                main()