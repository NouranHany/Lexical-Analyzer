from utils import graph_attr, save_as_json, render_graph

def add_state_to_group(groups, group_id, state):
    if group_id not in groups:
        groups[group_id] = [state]
    else:
        groups[group_id].append(state)
    return groups

def dfa_minimize(dfa):
    state_to_group = {}
    inputs = set() # hold all possible inputs
    groups = {}

    # Save the relation between groups and states
    for state in dfa:
        if state == "startingState":
            continue
        if dfa[state]["isTerminatingState"]:
            state_to_group[state] = "S1"
            groups = add_state_to_group(groups, "S1", state)
        else:
            state_to_group[state] = "S2"
            groups = add_state_to_group(groups, "S2", state)

        # Save all possible inputs
        for key in dfa[state]:
            if key == "isTerminatingState":
                continue
            else:
                inputs.add(key)

    converged = False
    while not converged:
        # assume convergence initially
        converged=True
        # Check that each group contains members that goes to same groups upon same inputs
        groups_names = list(groups.keys())
        for group in groups_names:
            for inputt in inputs:
                group_states = groups[group]
                has_input = False
                if inputt in dfa[group_states[0]]:
                    dest_group = state_to_group[dfa[group_states[0]][inputt]]
                    has_input = True
                for state in group_states[1:]:
                    confirm_has_input = inputt in dfa[state]
                    if has_input != confirm_has_input or (confirm_has_input and state_to_group[dfa[state][inputt]] != dest_group):
                        # a member goes to a destination other than the rest members in its group
                        # kick out of the group
                        converged = False
                        groups[group].remove(state)
                        state_to_group[state] = "S" + str(int(state_to_group[state][1:]) + 2)
                        groups = add_state_to_group(groups, state_to_group[state], state)

    minimized_dfa = {
        "startingState": state_to_group[dfa["startingState"]]
    }

    # Build the minimized dfa in the standard json format specified
    for group in groups:
        # Let the first state in the group be its representative state
        group_first_state = groups[group][0]
        # Equate the transitions of the group with the transitions of its representative state
        minimized_dfa[group] = dfa[group_first_state]
        for inputt in minimized_dfa[group]:
            if inputt == "isTerminatingState":
                continue
            # Change the name of the destination states to the name of their corresponding groups
            minimized_dfa[group][inputt] = state_to_group[minimized_dfa[group][inputt]]

    return minimized_dfa

dictionary = {
    "startingState": "S0",
    "S0": {
        "isTerminatingState": True,
        "a": "S2",
        "b": "S1"
    },
    "S1": {
        "isTerminatingState": True,
        "a": "S3",
        "b": "S1"
    },
    "S2": {
        "isTerminatingState": True,
        "a": "S2",
        "b": "S1"
    },
    "S3": {
        "isTerminatingState": True,
        "a": "S3",
        "b": "S4"
    },
    "S4": {
        "isTerminatingState": True,
        "a": "S3",
        "b": "S4"
    }
}

if __name__ == "__main__":
    minimized_dfa = dfa_minimize(dictionary)
    render_graph(minimized_dfa, filename="pattern", pattern="(a*b*)([a-b]*)", attr=graph_attr)
    save_as_json(minimized_dfa, filename="minimized_dfa")
