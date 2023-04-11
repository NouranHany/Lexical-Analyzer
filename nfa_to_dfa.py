def epsilon_enclosed(nfa,state):
    '''returns all the states that are reachable from the given state by ε'''
    states={state}
    stack=[state]
    while stack:
        popped_state=stack.pop()
        if "ε" in nfa[popped_state]:
            if type(nfa[popped_state]["ε"])== str:
                next_state=nfa[popped_state]["ε"]
                if next_state not in states:
                    stack.append(next_state)
                    states.add(next_state)
            else:
                for item in nfa[popped_state]["ε"]:
                    if item not in states:
                        stack.append(item)
                        states.add(item)
    return states


def rename(dfa):
    '''renames the states of the dfa to be in the form of S1,S2,S3, ... instead of the tuple of the states'''

    # creating  a dictionary which will be used to map from old name to new name
    dic={}
    index=1
    for state in dfa:
        if state!="startingState" and  state not in dic:
            dic[state]="S"+str(index)
            index+=1


    renamed_dfa=dfa.copy()
    for key in dfa:
        if key!="startingState":
            for mini_key in dfa[key]:
                if mini_key!="isTerminatingState":
                    renamed_state=dic[tuple(dfa[key][mini_key])]
                    # print("key ", key ," mini key ", mini_key , " renamed_state= ",renamed_state)
                    renamed_dfa[key][mini_key]=renamed_state
            renamed_state=dic[key]
            renamed_dfa[renamed_state]=renamed_dfa[key]
            del renamed_dfa[key]    
        else:
            renamed_state=dic[tuple(dfa[key])]
            renamed_dfa[key]=renamed_state
         
    return renamed_dfa



def nfa_to_dfa(nfa):
    '''converts the given nfa to dfa using subset construction algorithm'''
    dfa={}
    
    state=epsilon_enclosed(nfa,nfa["startingState"])
    dfa["startingState"]=state
    stack=[state]
    while stack:
        poped_state=stack.pop()
        dfa[tuple(poped_state)]={}
        # loop over each small state in the poped state
        # see all the new states generated for each action and append 
        # it in the dfa with the action/ terminal that lead to it 
        for small_state in poped_state:
            # print("state =",small_state)
            for keys in nfa[small_state]:
                if keys=="isTerminatingState":
                    if keys in dfa[tuple(poped_state)]:
                       dfa[tuple(poped_state)]["isTerminatingState"]=dfa[tuple(poped_state)]["isTerminatingState"]|nfa[small_state][keys]
                    else:
                       dfa[tuple(poped_state)]["isTerminatingState"]=nfa[small_state][keys] 
                elif keys!='ε':
                    next_states=epsilon_enclosed(nfa,nfa[small_state][keys])
                    if keys in dfa[tuple(poped_state)]:
                        dfa[tuple(poped_state)][keys].update(next_states)
                    else:
                        dfa[tuple(poped_state)][keys]=next_states

        # push new states that are not in dfa into the stack to be looped over
        for terminal in dfa[tuple(poped_state)]:
            if terminal!="isTerminatingState":
                new_state=dfa[tuple(poped_state)][terminal]
                if tuple(new_state) not in dfa:
                    stack.append(new_state)

    
    return rename(dfa)
