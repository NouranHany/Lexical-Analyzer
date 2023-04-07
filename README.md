# Lexical-Analyzer

This project is a Python-based lexical analyzer, consisting of two main files: `postfix.py` and `nfa.py`. It contain classes and functions for validating, pre-processing, and transforming regular expressions into postfix notation, as well as for constructing non-deterministic finite automata (NFAs) from postfix expressions.

## Transforming into Postfix
`postfix.py` contains a set of functions that validate regular expressions, preprocess them, and transform them into postfix notation using the Shunting-Yard algorithm.

### Functions
- `validate_regex`: Takes a regular expression as input and checks if it's valid. If it's not valid, it raises an error. If it's valid, it returns a cleaned-up version of the input.

- `replace_range`: Takes a regular expression as input and replaces any character ranges with the expanded character set. e.g [a-c] is transformed to a | b | c

- `add_concat`: Takes a preprocessed regular expression and inserts explicit concatenation operators.
- `fix_pattern`: Combines the above functions to take an input regular expression and return a cleaned-up, preprocessed version.

- `infix_to_postfix`: Takes a preprocessed regular expression and converts it into postfix notation using the Shunting-Yard algorithm.

## Constructing the NFA
`nfa.py` contains a class `NFA` that represents a non-deterministic finite automaton. The `NFA` class takes a postfix notation regular expression as input and builds the corresponding NFA using Thompson's Construction Algorithm. It contains functions that handle regular expression operations like concatenation, disjunction, one or more loops, zero or more loops, and zero or one.

### Class
- `NFA`: A class that represents a non-deterministic finite automaton. It has the following methods:

- `concatenate(self, other_nfa)`: Takes another NFA and concatenates it with the current NFA.
- `disjunction(self, other_nfa)`: Takes another NFA and constructs a new NFA that represents the disjunction of the two NFAs.
- `loop_one_or_more(self)`: Constructs a new NFA that represents the one or more loop of the current NFA.
- `loop_zero_or_more(self)`: Constructs a new NFA that represents the zero or more loop of the current NFA.
- `zero_or_one(self)`: Constructs a new NFA that represents the zero or one loop of the current NFA.
- `render_graph(self, filename)`: Renders the NFA as a graph and saves it to a file.

## Usage
Suppose we have the regular expression pattern `a(a|b)*b` 

We can transform this into postfix notation using the functions in `postfix.py`, as follows:

    ```python
    # Step 1: Set the pattern
    pattern = "a*(a|b)aa"
    # Step 2: Preprocess the pattern
    fixed_pattern = fix_pattern(pattern)
    # Step 3: Convert the pattern to postfix notation
    postfix_pattern = infix_to_postfix(fixed_pattern)
    ```

This results in the postfix pattern `aab|*.b.` We can then use this postfix expression to construct an NFA using the NFA class in `nfa.py`:

```python 
# Step 4: Build the NFA
nfa = construct_nfa(postfix_pattern)
# Step 5: Render the NFA as a graph
nfa.render_graph(filename="pattern")
```
This will render the following NFA graph:
<p align="center">
  <img src="https://user-images.githubusercontent.com/59095993/218258760-82d70b5c-56d2-4820-8644-4d5a1fb68a6b.jpg" width=400 alt="Machathon header">
</p>

## Contributors
<table align="center">
  <tr>
    <td align="center">
    <a href="https://github.com/Halahamdy22" target="_black">
    <img src="https://avatars.githubusercontent.com/u/56937106?v=4" width="100px;" alt="Hala Hamdy"/>
    <br />
    <sub><b>Hala Hamdy</b></sub></a>
    </td>
    <td align="center">
    <a href="https://github.com/NouranHany" target="_black">
    <img src="https://avatars.githubusercontent.com/u/59095993?v=4" width="100px;" alt="Noran Hany"/>
    <br />
    <sub><b>Noran Hany</b></sub></a>
    </td>
  </tr>
 </table>