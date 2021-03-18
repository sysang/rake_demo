import yake

from rake_nltk import Rake

from keybert import KeyBERT
from flair.embeddings import TransformerDocumentEmbeddings

from nltk.corpus import stopwords

import spacy
import pytextrank


def rake_impl(text, language='nl'):
    languages = {'en': 'english', 'nl': 'dutch'}
    lang = languages[language]
    stop_words = stopwords.words(lang)

    r = Rake(language=languages[language], min_length=1, max_length=3, stopwords=stop_words)
    r.extract_keywords_from_text(text)
    keywords = r.get_ranked_phrases_with_scores()

    kws = []
    for kw in list(keywords):
        kws.append((kw[1], kw[0]))

    return kws


def yake_impl(text, language='nl'):
    max_ngram_size = 3
    deduplication_thresold = 0.9
    deduplication_algo = 'seqm'
    windowSize = 1
    numOfKeywords = 20

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
    languages = {'en': 'english', 'nl': 'dutch'}
    lang = languages[language]

    # bert = TransformerDocumentEmbeddings('bert-base-multilingual-cased')
    bert = TransformerDocumentEmbeddings('henryk/bert-base-multilingual-cased-finetuned-dutch-squad2')
    model = KeyBERT(model=bert)

    stop_words = stopwords.words(lang)

    keywords = model.extract_keywords(text, keyphrase_ngram_range=(1, 3), stop_words=stop_words, use_maxsum=False, nr_candidates=20, top_n=20)

    return keywords


def textrank_impl(text, language='nl'):
    # load a spaCy model, depending on language, scale, etc.
    nlp = spacy.load("nl_core_news_md")

    # add PyTextRank to the spaCy pipeline
    nlp.add_pipe("textrank", last=True)
    doc = nlp(text)

    keywords = []
    for p in doc._.phrases:
        keywords.append((p.text, p.rank))

    return keywords
