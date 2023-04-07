from graphviz import Digraph

import os
os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin/'

last_state = 0

def generate_state():
    global last_state
    last_state+=1
    return "S" + str(last_state)

class NFA:
    def __init__(self, start_state, end_state, state_input):
        self.start_state = start_state
        self.end_state = end_state
        self.states = {
            self.start_state: {
                state_input: [end_state]
            },
            self.end_state: {}
        }

    def connect_with_epsilon(self, from_state, to_state):
        if "ε" in self.states[from_state]:
            self.states[from_state]["ε"].append(to_state)
        else:
            self.states[from_state]["ε"] = [to_state]

    def concatenate(self, NFA2):
        self.connect_with_epsilon(self.end_state, NFA2.start_state)
        self.states.update(NFA2.states)
        self.end_state = NFA2.end_state

    def disjunction(self, NFA2):
        start_state = generate_state()
        end_state = generate_state()

        self.states[start_state] = {"ε": [self.start_state, NFA2.start_state]}
        self.states[end_state] = {}

        self.connect_with_epsilon(self.end_state, end_state)
        NFA2.connect_with_epsilon(NFA2.end_state, end_state)

        self.states.update(NFA2.states)

        self.start_state = start_state
        self.end_state = end_state

    def loop_one_or_more(self):
        start_state = generate_state()
        end_state = generate_state()

        self.connect_with_epsilon(self.end_state, self.start_state)
        self.connect_with_epsilon(self.end_state, end_state)

        self.states[start_state] = {"ε": [self.start_state]}
        self.states[end_state] = {}

        self.start_state = start_state
        self.end_state = end_state

    def loop_zero_or_more(self):
        self.loop_one_or_more()
        self.connect_with_epsilon(self.start_state, self.end_state)

    def zero_or_one(self):
        self.connect_with_epsilon(self.start_state, self.end_state)

    def render_graph(self, filename, pattern):
        gra = Digraph(graph_attr={'rankdir':'LR', 'bgcolor':'#6169F8'})
        # Add the nodes to the graph
        for state in self.states:
            shape = "doublecircle" if state == self.end_state else "circle"
            gra.node(state, shape=shape, style='filled', fillcolor='#89FCE2')

        # Add the edges to the graph
        for from_state in self.states:
            for input in self.states[from_state]:
                for to_state in self.states[from_state][input]:
                    gra.edge(tail_name=from_state, head_name=to_state, label=input, color='yellow')

        gra.attr(label="The NFA for the pattern: " + pattern, fontcolor='white', fontname='bold', fontsize='20')
        gra.render(filename, view=True)

def construct_nfa(postfix_reg):
    stack = []
    for symbol in postfix_reg:
        if symbol == "|":
            nfa_right = stack.pop()
            nfa_left = stack.pop()
            nfa_left.disjunction(nfa_right)
            stack.append(nfa_left)
        elif symbol == ".":
            nfa_right = stack.pop()
            nfa_left = stack.pop()
            nfa_left.concatenate(nfa_right)
            stack.append(nfa_left)
        elif symbol == "*":
            nfa = stack.pop()
            nfa.loop_zero_or_more()
            stack.append(nfa)
        elif symbol == "+":
            nfa = stack.pop()
            nfa.loop_one_or_more()
            stack.append(nfa)
        elif symbol == "?":
            nfa = stack.pop()
            nfa.zero_or_one()
            stack.append(nfa)
        else:
            nfa = NFA(start_state=generate_state(), end_state=generate_state(), state_input=symbol)
            stack.append(nfa)

    return stack.pop()
