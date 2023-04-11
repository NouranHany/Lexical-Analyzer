from postfix import fix_pattern, infix_to_postfix
from nfa import construct_nfa
from utils import render_graph, save_as_json, graph_attr

if __name__ == "__main__":
        # Step 1: Set the pattern
        pattern = "(a*b*)([a-b]*)"
        # Step 2: Preprocess the pattern
        fixed_pattern = fix_pattern(pattern)
        # Step 3: Convert the pattern to postfix notation
        postfix_pattern = infix_to_postfix(fixed_pattern)
        # Step 4: Build the NFA
        nfa = construct_nfa(postfix_pattern)
        # Step 5: Render the NFA as a graph
        render_graph(nfa, filename="pattern", pattern=pattern, attr=graph_attr)
        # Step 6: Save into a Json file
        save_as_json(nfa, filename="nfa")
