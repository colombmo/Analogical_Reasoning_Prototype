# Analogical Reasoning Prototype

A prototype for Fuzzy Analogical Reasoning [1], using Colombo and Portmann [2] semantic similarity measure, and ConceptNet.

This prototype demonstrate reasoning by analogy on nouns and concepts, using conceptual analogies, and reasoning by analogy on adjectives, using spectral analogies, as presented in [3].

The latter is the main contribution of this project, and uses a "Computing With Words"-based [4] measure computing how close the meaning of two adjectives are in the spectrum of all the words describing the same feature.

## Installation

- Make sure you have Python 3.X installed
- Creating a virtual environment (e.g., using `virtualenv`) to run this project is suggested
- Install the necessary packages with `pip install -r requirements.txt`

## Running the prototype

- From the main folder of the project, input `python main.py` to start the prototype
- In the prototype, insert the wanted analogies as `a:b::c:?` or `A(a,b):B(c,?)`. Example: `chapter:book::city:?` or `Ferrari(fast, expensive):Fiat(slow, ?)`



## References

[1] S. D’Onofrio, S. M. Müller, E. I. Papageorgiou, and E. Portmann.  "Fuzzy Reasoning in Cognitive Cities: An Exploratory Work on Fuzzy Analogical Reasoning Using Fuzzy Cognitive Maps." 2018 IEEE International Conference on Fuzzy Systems (FUZZ-IEEE). IEEE, 2018.

[2] M. Colombo, and E. Portmann. "Semantic Similarity Between Adjectives and Adverbs—The Introduction of a New Measure." Soft Computing for Biomedical Applications and Related Topics. Springer, Cham, 2020. 103-116.

[3] M. Colombo, S. D’Onofrio and E. Portmann, "Integration of Fuzzy Logic in Analogical Reasoning: A Prototype," 2020 IEEE 16th International Conference on Intelligent Computer Communication and Processing (ICCP), 2020, pp. 5-11, doi: 10.1109/ICCP51029.2020.9266156.

[4] L. A. Zadeh. "Fuzzy logic= computing with words." Computing with Words in Information/Intelligent Systems 1. Physica, Heidelberg, 1999. 3-23.
