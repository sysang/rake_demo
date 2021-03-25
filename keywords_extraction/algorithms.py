import yake
import re

from rake_nltk import Rake

from nltk.corpus import stopwords

import spacy
import pytextrank

from .keysbert import KeySBERT
from .utils import PREPOSITIONS_ARTICLES


def rake_impl(text, language='nl'):
    languages = {'en': 'english', 'nl': 'dutch'}
    lang = languages[language]
    stop_words = stopwords.words(lang)

    top_n = 5

    r = Rake(language=languages[language], min_length=1, max_length=2, stopwords=stop_words)
    r.extract_keywords_from_text(text)
    keywords = r.get_ranked_phrases_with_scores()

    kws = []
    for kw in list(keywords):
        kws.append((kw[1], kw[0]))

    return kws[0:top_n]


def yake_impl(text, language='nl'):
    max_ngram_size = 2
    deduplication_thresold = 0.9
    deduplication_algo = 'seqm'
    windowSize = 1
    numOfKeywords = 5

    custom_kw_extractor = yake.KeywordExtractor(
            lan=language,
            n=max_ngram_size,
            dedupLim=deduplication_thresold,
            dedupFunc=deduplication_algo,
            windowsSize=windowSize,
            top=numOfKeywords,
            features=None)
    keywords = custom_kw_extractor.extract_keywords(text)

    return reversed(keywords)


def keybert_impl(text, language='nl'):
    # languages = {'en': 'english', 'nl': 'dutch'}
    # lang = languages[language]
    top_n = 20

    model = KeySBERT("distiluse-base-multilingual-cased-v1")

    keywords = model.extract_keyphrases(text, top_n)

    return keywords


def textrank_impl(text, language='nl'):
    # load a spaCy model, depending on language, scale, etc.
    nlp = spacy.load("nl_core_news_md")

    top_n = 15

    # add PyTextRank to the spaCy pipeline
    nlp.add_pipe("textrank", last=True)
    doc = nlp(text)

    regex = re.compile(r'(\w|,)+\s')

    keywords = []
    cache = []
    ind = 1
    for p in doc._.phrases:
        k = p.text.lower()

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

        if k not in cache:
            cache.append(k)
            keywords.append((k, p.rank))
            ind += 1

        if ind > top_n:
            break

    return keywords


if __name__ == "__main__":
    keybert_impl('test')
