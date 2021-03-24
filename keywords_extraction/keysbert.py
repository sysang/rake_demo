"""
Copyright (c) 2020, Maarten P. Grootendorst
Copyrights licensed under MIT License
Project: https://github.com/MaartenGr/KeyBERT
File: https://github.com/MaartenGr/KeyBERT/blob/v0.2/keybert/model.py
"""

from typing import List, Union, Tuple
import re

import spacy
from sklearn.metrics.pairwise import cosine_similarity

from sentence_transformers import SentenceTransformer

from .utils import PREPOSITIONS_ARTICLES


class KeySBERT:
    """
    A minimal method for keyword extraction with BERT

    The keyword extraction is done by finding the sub-phrases in
    a document that are the most similar to the document itself.

    - First, document embeddings are extracted with BERT to get a
    document-level representation.
    - Then, Spacy is used to extract words/phrases.
    - Finally, we use cosine similarity to find the
    words/phrases that are the most similar to the document.

    The most similar words could then be identified as the words that
    best describe the entire document.

    """
    def __init__(self, model_name: str = 'distilbert-base-nli-mean-tokens'):
        """ KeySBERT initialization """

        self.model = SentenceTransformer(model_name, device='cpu')

    def extract_keyphrases(
            self,
            docs: Union[str, List[str]],
            top_n: int = 10) -> Union[List[Tuple[str, float]], List[List[Tuple[str, float]]]]:

        try:
            nlp = spacy.load("nl_core_news_md")
            docobj = nlp(docs)
            phrases = [str(w) for w in docobj.noun_chunks]
            words = self.filter_keyphrases(phrases)

            # Extract Embeddings
            doc_embedding = self.model.encode([docs])
            word_embeddings = self.model.encode(words)

            distances = cosine_similarity(doc_embedding, word_embeddings)
            keywords = [(words[index], round(float(distances[0][index]), 4))
                        for index in distances.argsort()[0][-top_n:]][::-1]

            return keywords

        except ValueError:
            return []

    def filter_keyphrases(self, phrases):
        regex = re.compile(r'\w+\s')

        result = []
        for p in phrases:

            k = p.lower()

            s = regex.match(k)
            if s:
                matched = s.group(0).strip()

                while matched in PREPOSITIONS_ARTICLES:
                    span = s.span(0)
                    k = k[span[1]:]

                    s = regex.match(k)
                    if s:
                        matched = s.group(0).strip()
                    else:
                        matched = None

            if k not in result:
                result.append(k)

        return result
