from postfix import fix_pattern, infix_to_postfix
from nfa import construct_nfa

if __name__ == "__main__":
    # Step 1: Set the pattern
    pattern = "a*(a|b)aa"
    # Step 2: Preprocess the pattern
    fixed_pattern = fix_pattern(pattern)
    # Step 3: Convert the pattern to postfix notation
    postfix_pattern = infix_to_postfix(fixed_pattern)
    # Step 4: Build the NFA
    nfa = construct_nfa(postfix_pattern)
    # Step 5: Render the NFA as a graph
    nfa.render_graph(filename="pattern", pattern=pattern)