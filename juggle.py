from itertools import combinations
import networkx as nx
import matplotlib.pyplot as plt

def node_formatter(state):
    return '.'.join(map(str, state))
class valid_states:
    def __init__(s, balls = 2, max_height = 3):
        s.balls = balls
        s.max_height = max_height
        s.valid_states = [sorted(x) for x in combinations(range(1,s.max_height+1), balls)]
        s.directed_edges = []
        for state in s.valid_states:
            s.directed_edges += calculate_possible_throws(state, balls = s.balls, max_height=s.max_height)
        s.string_nodes = [node_formatter(x) for x in s.valid_states]
        s.string_directed_edges = [(node_formatter(x[0]), node_formatter(x[1]), str(x[2])) for x in s.directed_edges]
    def visualize(s, filter_zero_throws = False):
        if filter_zero_throws == False:
            de = s.string_directed_edges
        elif filter_zero_throws:
            de = [x for x in s.string_directed_edges if x[2] != '0']
            
        plot_network(nodes=s.string_nodes, directed_edges=de)

def shift_by_one_and_filter_zero(state):
    end = [x - 1 for x in state if x > 1]
    return sorted(end)
def toss(state, height = None):
    if (height != None) and (height > 0 ) and (height + 1 in state):
        raise Exception('a throw of this height will cause a collision')
    match sorted(state):
        case [1, *rest]:
            if not height:
                raise Exception('height must be specified for non-zero throw')
            else:
                return sorted( shift_by_one_and_filter_zero(state) + [height, ])
        case _:
            return sorted( shift_by_one_and_filter_zero(state) )




def calculate_possible_throws(state, balls = 2, max_height = 3):
    possible_throws = []
    if 1 not in state:
        possible_throws.append([state , toss(state, height = 0 ), 0 ])
        return possible_throws
    else:
        shifted_state = shift_by_one_and_filter_zero(state)
        possible_heights = [x for x in range(1, max_height + 1) if x not in shifted_state]
        for possible_height in possible_heights:
            possible_throws.append([state, toss(state, height = possible_height), possible_height])
        return possible_throws
def plot_network( nodes = None, directed_edges = None):
    
    plt.figure(figsize=(20, 10))
    # Create directed graph
    G = nx.DiGraph()

    # Add nodes
    nodes = nodes

    G.add_nodes_from(nodes)

    # Add directed edges and labels
    edges = directed_edges

    for source, target, label in edges:
        G.add_edge(source, target, label=label)
    pos = nx.spring_layout(
        G,
        k=10,
        iterations=200,
        seed=42,
        scale = 5
    )
    # Normal nodes
    nx.draw_networkx_nodes(
        G,
        pos,
        node_size=800,
        node_color="white",
        edgecolors="black"
    )
    
    # Directed edges
    nx.draw_networkx_edges(
        G,
        pos,
        arrows=True,
        arrowstyle="-|>",
        arrowsize=18,
        edge_color="black",
        node_size=800,
        connectionstyle="arc3,rad=0.3"
    )
    
    # Node labels
    nx.draw_networkx_labels(
        G,
        pos,
        font_size=10
    )
    
    # Edge labels
    edge_labels = nx.get_edge_attributes(G, "label")
    
    nx.draw_networkx_edge_labels(
        G,
        pos,
        edge_labels=edge_labels,
        font_size=7,
        label_pos=0.5,
        connectionstyle="arc3,rad=0.3"
    )
    
    plt.axis("off")
    plt.tight_layout()
    plt.show()

