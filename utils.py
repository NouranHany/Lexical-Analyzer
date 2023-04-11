from graphviz import Digraph
import os
import json
os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin/'

graph_attr = { 
        "bgcolor": "#6169F8",
        "node_fillcolor": "#89FCE2",
        "edge_color": "yellow",
        "label_fontcolor": "white",
        "label_fontsize": "20"
        }

def render_graph(finite_automata, filename, pattern, attr):
    '''
    Renders the NFA as a graph and saves it to a file.
    '''
    gra = Digraph(graph_attr={'rankdir':'LR', 'bgcolor': attr["bgcolor"]})
    # Add the nodes to the graph
    for state in finite_automata:
        if state == "startingState":
            gra.node(state, style='invisible')
        else:
            shape = "doublecircle" if finite_automata[state]["isTerminatingState"] else "circle"
            gra.node(state, shape=shape, style='filled', fillcolor= attr["node_fillcolor"])

    # Add the edges to the graph
    for from_state in finite_automata:
        if from_state == "startingState":
            gra.edge(tail_name=from_state, head_name=finite_automata["startingState"], color=attr["edge_color"])
            continue

        for input in finite_automata[from_state]:
            if input == "isTerminatingState":
                continue
            to_states = finite_automata[from_state][input]
            # Decide to Draw edge or edges based on 
            # whether have a single destination or a list of destinations
            if type(to_states) == list:
                for to_state in to_states:
                    gra.edge(tail_name=from_state, head_name=to_state, label=input, color=attr["edge_color"])
            else:
                gra.edge(tail_name=from_state, head_name=to_states, label=input, color=attr["edge_color"])

    gra.attr(label="The NFA for the pattern: " + pattern, fontcolor=attr["label_fontcolor"], fontname='bold', fontsize=attr["label_fontsize"])
    gra.render(filename, view=True)

def save_as_json(dictionary, filename):
    # Serializing json
    json_object = json.dumps(dictionary, indent=4)
    
    # Writing to sample.json
    with open(filename + ".json", "w") as outfile:
        outfile.write(json_object)