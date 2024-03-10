import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Assigns attributes to columns in data
def assign_attributes(file_name):
  attributes = [
  "ID", "STime", "Flags", "Protocol", "SourceIP", "SourcePort", "DestinationIP", "DestinationPort",
  "Packets", "Bytes", "State", "LastTime", "Sequence", "Duration", "Mean", "Stddev", "Min", "Max", 
  "Spkts", "Dpkts", "Sbytes", "Dbytes", "Rate", "Srate", "Drate", "TnBPSrcIP", "TnBPDstIP", "TnP_PSrcIP",
  "TnP_PDstIP", "AR_P_Proto_P_Sport", "Pkts_P_State_P_Protocol_P_DestIP", "Pkts_P_State_P_Protocol_P_SrcIP", 
  "Attack", "Category", "Subcategory"
  ]
  
  raw_data = pd.read_csv(file_name, low_memory = False)
  raw_data.columns = attributes
  return raw_data

formatted_data = assign_attributes("UNSW_2018_IoT_Botnet_Dataset_1.csv")

# ---------- Part 1 ----------
correlation_matrix = formatted_data.corr()
print(correlation_matrix)


# ---------- Part 2: Representing the graph using different nodes and edges ----------
# Plots a graph with given data, and node and edge attributes
def representation(data, node, edge):
  Graph = nx.from_pandas_edgelist(data, node, edge, create_using = nx.DiGraph())
  pos = nx.circular_layout(Graph)
  nx.draw(Graph, pos, with_labels = True, font_weight = "bold", node_size = 700, node_color = "green", 
          font_size = 8, edge_color = "red", linewidths = 0.5, font_color = "purple")
  plt.show()

representation(formatted_data, "SourceIP", "Attack") # First representation
representation(formatted_data, "Attack", "SourceIP") # Second representation
representation(formatted_data, "SourceIP", "Protocol") # Third representation

# Fourth representation
user_node = input("Enter the attribute that will be used as a node: ") # For example: SourceIP
user_edge = input("Enter the attribute that will be used as an edge: ") # For example: State
representation(formatted_data, user_node, user_edge)


# ---------- Part 3: DFS and calculating packets ----------
def find_path(Graph, start, end):
  path = nx.shortest_path(Graph, source = start, target = end)
  return path

def calculate_packets(Graph, path):
  packets = 0

  for i in range(len(path) - 1):
    origin = path[i]
    destination = path[i + 1]

    if Graph.has_edge(origin, destination):
      packets += Graph[origin][destination]["Packets"]
    else:
      print(f"Warning: No direct edge between {origin} and {destination}")

  return packets

Graph = nx.from_pandas_edgelist(formatted_data, "SourceIP", "DestinationIP", ["Attack", "Packets"], 
                                create_using = nx.DiGraph())
graph_dict = dict(Graph.adjacency())

origin = "192.168.100.150"
destination = "192.168.217.2"

path = find_path(Graph, origin, destination)

print("\n", end = "")
if path:
  print(f"Path from {origin} to {destination}: ", end = "")
  for ip in path:
    if ip != path[-1]:
      print(f"{ip} -> ", end = "")
    else:
      print(ip)
  
  packets = calculate_packets(Graph, path)
  print(f"Total number of sent packets: {packets}")
else:
  print(f"No path found from {origin} to {destination}")
print("\n", end = "")

# Drawing the graph of the path
path_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
path_graph = Graph.edge_subgraph(path_edges)
pos = nx.spring_layout(path_graph)
nx.draw(path_graph, pos, with_labels=True, font_weight="bold", font_size = 8, node_color="green", 
        node_size = 700, edge_color = "red", font_color = "purple")
plt.show()

# ---------- Part 4: Differentiating protocols ----------
def representation_with_colors(data, node, edge, colors):
  Graph = nx.from_pandas_edgelist(data, node, edge, create_using = nx.DiGraph())
  
  source_ip_colors = {ip: color for ip, color in zip(data["Protocol"].unique(), colors)}
  node_colors = [source_ip_colors.get(ip, "green") for ip in Graph.nodes()]

  pos = nx.circular_layout(Graph)
  nx.draw(Graph, pos, with_labels = True, font_weight = "bold", node_size = 700, node_color = node_colors,
      edge_color = "red", font_size = 8, linewidths = 0.5, font_color = "purple")

  plt.show()

colors = ["", "", "", "", ""] # For example: yellow, blue, orange, gray, red
protocols = ["tcp", "udp", "arp", "icmp", "ipv6-icmp"]

for index in range(5):
  color = input(f"Enter the color for the protocol {protocols[index]}: ")
  colors[index] = color

representation_with_colors(formatted_data, "SourceIP", "Protocol", colors)


Graph = nx.from_pandas_edgelist(formatted_data, "SourceIP", "DestinationIP", ["Attack", "Packets"], create_using=nx.DiGraph())
# ---------- Part 5: Values of parameters of the Graph ----------
def plot_xy_graph(quantity, graph_name, x_label, y_label):
  quantity_nodes = list(quantity.keys())
  quantity_values = list(quantity.values())

  plt.scatter(quantity_nodes, quantity_values, s = 5)
  plt.title(graph_name)
  plt.xlabel(x_label)
  plt.ylabel(y_label)
  plt.show()


# Degree connectivity
degree_connectivity = nx.degree_centrality(Graph)
plot_xy_graph(degree_connectivity, "Degree Connectivity Graph", "IPs", "Degree Connectivity")

# Closeness connectivity
closeness_centrality = nx.closeness_centrality(Graph)
plot_xy_graph(closeness_centrality, "Closeness Centrality Graph", "IPs", "Closeness Centrality")

# Betweenness centrality
betweenness_centrality = nx.betweenness_centrality(Graph)
plot_xy_graph(betweenness_centrality, "Betweenness Centrality Graph", "IPs", "Betweenness Centrality")

# Network Density
network_density = nx.density(Graph)
print("Network Density:", network_density)

# Network Diameter and Network average Path Length
largest_strongly_connected_component = max(nx.strongly_connected_components(Graph), key=len)
subgraph = Graph.subgraph(largest_strongly_connected_component)

network_diameter = nx.diameter(subgraph)
average_path_length = nx.average_shortest_path_length(subgraph)
print("Network Diameter:", network_diameter)
print("Network Average Path Length:", average_path_length)