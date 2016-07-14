# markov-python
A better(?) Markov text generator for Python

parse.py takes a text file and a unique name as input, and parses the text. The parsed text goes into a special .db file, which is used by markov.py.

markov.py accepts the name used for parse.py, and generates random sentences based off of the parsed text from parse.py.


Markov text generators read the text word by word. The generator maintains, for each word, a list of words that come after it in the text. For example, the text "The quick brown fox jumps over the lazy dog" would create a table like this:

    "the"   | "quick", "lazy"
    "quick" | "brown"
    "brown" | "fox"
    "fox"   | "jumps"
    "jumps" | "over"
    "over"  | "the"
    "lazy"  | "dog"
    "dog"   |

The generator would take this table, and randomly select a starting word. If the starting word was "the", then several sentences could result. The original sentence is a possibility, but so is:

    "the lazy dog"
    "the quick brown fox jumps over the quick brown fox jumps over the lazy dog"

Some examples taken from the entire text of A Tale Of Two Cities by Dickens, from Project Gutenburg:

    They were at his mind he moved after all the shop kept an old trial at first, then and could
    He is arrived at the chair a patient was far off, some breaking silence those blue cap to discharge of
    not in his closet and the right all through his sacred the jar of wood and that I am come
    subject of Paris, streets were right, by strange feet and were so he expressly to be obliterated marks of tears,
    getting over on his pint of a third comes up from making paper on direct responsibility for their scanty measures
