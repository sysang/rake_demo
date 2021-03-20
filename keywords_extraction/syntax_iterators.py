from typing import Union, Iterator

from ...symbols import NOUN, PROPN, PRON, ADJ, VERB
from ...errors import Errors
from ...tokens import Doc, Span


def noun_chunks(doclike: Union[Doc, Span]) -> Iterator[Span]:
    """
    Detect base noun phrases from a dependency parse. Works on both Doc and Span.
    """

    """
    doclike:
        is instance of <class 'spacy.tokens.doc.Doc'>
        print(doclike) -> processing input text

    [for i, word in enumerate(doclike)]:
        word:
            is instance of <class 'spacy.tokens.token.Token'>

        word.i:
            The index of the token within the parent document. 

        word.dep: 
            Syntactic dependency relation

        word.head:
            is instance of <class 'spacy.tokens.token.Token'>
            The syntactic parent, or “governor”, of this token. 
            In linguistics, the head or nucleus of a phrase is the word that determines the syntactic category of that phrase.
            For example, the head of the noun phrase boiling hot water is the noun water.

        word.left_edge:
            is instance of <class 'spacy.tokens.token.Token'>
            for each item (as a constituent word) of doclike,
            it comprises a certain phrase if its left_edge.i is equal to another's left_edge.i
            or is between two equal left_edge.i(s)

        word.pos:
            word type (denoted by number, see: https://github.com/explosion/spaCy/blob/master/spacy/symbols.pxd
     """

    labels = [
        # "oprd", # object predicate
        "nsubj", # nominal subject
        "nsubj:pass", # nominal subject
        "dobj", # direct object
        "obj", # direct object
        "obl:agent", # oblique object:agent
        "acl:relcl", # clausal modifier of noun:relative clause modifier
        # "nsubjpass", # nominal subject passive
        # "pcomp", # complement of preposition
        # "pobj", # object of preposition
        # "dative", # dative, https://en.wikipedia.org/wiki/Dative_case
        # "appos", # appositional, https://en.wikipedia.org/wiki/Apposition
        # "attr", # attribute
        # "ROOT", # root
    ]

    # conj -> conjuct, https://en.wikipedia.org/wiki/Conjunct
    # NP -> noun phrase
    # PROPN -> proper noun
    # PRON -> pronoun
    # nmod -> nominal modifier
    # obj -> object
    # ccomp -> clausal complement

    doc = doclike.doc  # Ensure works on both Doc and Span.
    if not doc.has_annotation("DEP"):
        raise ValueError(Errors.E029)

    # np_deps is of kind similar to [433, 429, 416, 430, 438, 439, 3965108062993911700, 403, 404, 8206900633647566924]
    # doc.vocal.strings : StringStore :Look up strings by 64-bit hashes.
    # https://spacy.io/api/stringstore
    # doc.vocal.strings.add : Add a string to the StringStore -> return: The string’s hash value.
    np_deps = [doc.vocab.strings.add(label) for label in labels]

    # a representative (hashed) number for conj
    conj = doc.vocab.strings.add("conj")
    np_label = doc.vocab.strings.add("NP")
    punct = doc.vocab.strings.add("punct")
    nmod = doc.vocab.strings.add("nmod")
    nsubj = doc.vocab.strings.add("nsubj")
    obj = doc.vocab.strings.add("obj")
    obl = doc.vocab.strings.add("obl")
    case = doc.vocab.strings.add("case")
    appos = doc.vocab.strings.add("appos")
    ROOT = doc.vocab.strings.add("ROOT")
    det = doc.vocab.strings.add("det")
    ccomp = doc.vocab.strings.add("ccomp")

    # initial reasonable value, no other logic
    # prev_end = -1

    # Loop over the text to process each word
    for i, word in enumerate(doclike):
        print("\n-  {}".format(str(word)))
        print("\t{}..[{}]; (dep)[{}, {}]; (head){} (POS){}".format(word.left_edge.i, word.i, word.dep, word.dep_, word.head, word.pos_))

        # word.pos -> part of speech of token
        # pos must be one of NOUN, PRONP, or PRON
        if word.pos not in (NOUN, PROPN, PRON, ADJ, VERB):
            continue

        # Prevent nested chunks from being produced
        # if word.left_edge.i < prev_end:
            # continue

        # if token's dependency is one of syntactic type then
        # this word is previous end of next word of phrase
        # return
        if word.dep in np_deps and word.left_edge.dep != punct:
            yield word.left_edge.i, word.i + 1, np_label
            print("   (NP1) {}".format(word))

        # or else, if check whether word's dependency is conjunct then
        # recursively catch the final head of phrase
        # check if head's dependency is one of syntactic type to return
        elif word.dep == appos:
            head = word.head

            # recursively set head of children
            while head.dep == appos and head.head.i < head.i:
                head = head.head

            # If the head is an NP, and we're coordinated to it, we're an NP
            if head.dep in np_deps:
                yield word.left_edge.i, word.i + 1, np_label
                print("   (NP5) {}".format(word))
            elif head.dep == nmod:
                yield word.head.left_edge.i, word.i + 1, np_label
                print("   (NP6) {}".format(word))

        # Process sytax for NP with PP
        # if token is nominal modifier(nmod) and its left edge is preposition
        # then check if its head is obj
        elif word.dep == nmod and (word.left_edge.dep in (case, det) or word.i == word.left_edge.i) and word.head.dep in (obj, nsubj, ROOT):
            yield word.head.left_edge.i, word.i + 1, np_label
            print("   (NP2) {} <- {}".format(word, word.head.left_edge.i))

        # Process syntax for oblique object
        # Case 1: oblique object has clausal complement(ccomp)
        # Case 2: without ccomp
        elif word.dep == obl:
            if word.head.dep == ccomp:
                yield word.head.left_edge.i, word.i + 1, np_label
                print("   (NP3) {}".format(word))
            elif word.left_edge.dep != punct:
                yield word.left_edge.i, word.i + 1, np_label
                print("   (NP4) {}".format(word))


    # TODO Study the use of the return left_edge, i + 1, np_label


SYNTAX_ITERATORS = {"noun_chunks": noun_chunks}
