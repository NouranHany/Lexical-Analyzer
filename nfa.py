
last_state = 0

def generate_state():
    global last_state
    last_state+=1
    return "S" + str(last_state)

class NFA:
    def __init__(self, start_state, end_state, state_input):
        '''
        A class that represents a non-deterministic finite automaton.
        '''
        self.start_state = start_state
        self.end_state = end_state
        self.states = {
            self.start_state: {
                state_input: end_state
            },
            self.end_state: {}
        }

    def connect_with_epsilon(self, from_state, to_state):
        if "ε" in self.states[from_state]:
            if type(self.states[from_state]["ε"]) == list:
                self.states[from_state]["ε"].append(to_state)
            else:
                self.states[from_state]["ε"]= [self.states[from_state]["ε"], to_state]
        else:
            self.states[from_state]["ε"] = to_state

    def concatenate(self, other_nfa):
        '''
        Takes another NFA and concatenates it with the current NFA.
        '''
        self.connect_with_epsilon(self.end_state, other_nfa.start_state)
        self.states.update(other_nfa.states)
        self.end_state = other_nfa.end_state

    def disjunction(self, other_nfa):
        '''
        Takes another NFA and constructs a new NFA 
        that represents the disjunction of the two NFAs.
        '''
        start_state = generate_state()
        end_state = generate_state()

        self.states[start_state] = {"ε": [self.start_state, other_nfa.start_state]}
        self.states[end_state] = {}

        self.connect_with_epsilon(self.end_state, end_state)
        other_nfa.connect_with_epsilon(other_nfa.end_state, end_state)

        self.states.update(other_nfa.states)

        self.start_state = start_state
        self.end_state = end_state

    def loop_one_or_more(self):
        '''
        Constructs a new NFA that represents the one or more loop of the current NFA.
        '''
        start_state = generate_state()
        end_state = generate_state()

        self.connect_with_epsilon(self.end_state, self.start_state)
        self.connect_with_epsilon(self.end_state, end_state)

        self.states[start_state] = {"ε": self.start_state}
        self.states[end_state] = {}

        self.start_state = start_state
        self.end_state = end_state

    def loop_zero_or_more(self):
        '''
        Constructs a new NFA that represents the zero or more loop of the current NFA.
        '''
        self.loop_one_or_more()
        self.connect_with_epsilon(self.start_state, self.end_state)

    def zero_or_one(self):
        '''
        Constructs a new NFA that represents the zero or one loop of the current NFA.
        '''
        self.connect_with_epsilon(self.start_state, self.end_state)

    def to_finite_automata_format(self):
        '''
        Convert states from python dictionary to json format
        '''
        # Make a copy of the states dictionary
        states = self.states
        # Add the "is terminating state"
        for state in states:
            states[state]["isTerminatingState"] = state == self.end_state
        # Add the "starting state"
        states.update({"startingState": self.start_state})
        # Convert to json
        return states

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

    final_nfa = stack.pop()
    return final_nfa.to_finite_automata_format()
