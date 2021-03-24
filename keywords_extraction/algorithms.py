import yake
import re

from rake_nltk import Rake

from keybert import KeyBERT
from sentence_transformers import SentenceTransformer

from nltk.corpus import stopwords

import spacy
import pytextrank


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
    languages = {'en': 'english', 'nl': 'dutch'}
    lang = languages[language]
    nr_candidates = 20
    top_n = 10

    # bert = TransformerDocumentEmbeddings('henryk/bert-base-multilingual-cased-finetuned-dutch-squad2')
    # bert = TransformerDocumentEmbeddings('nlptown/bert-base-multilingual-uncased-sentiment')
    # model = KeyBERT(model=bert)

    sentence_model = SentenceTransformer("distiluse-base-multilingual-cased-v1", device="cpu")
    model = KeyBERT(model=sentence_model)

    stop_words = stopwords.words(lang)

    keywords = model.extract_keywords(
        text,
        keyphrase_ngram_range=(1, 3),
        stop_words=stop_words,
        nr_candidates=nr_candidates, top_n=top_n,
        use_maxsum=True,
        )

    return sorted(keywords, key=lambda k: k[1], reverse=True)


def textrank_impl(text, language='nl'):
    # load a spaCy model, depending on language, scale, etc.
    nlp = spacy.load("nl_core_news_md")

    top_n = 15

    # add PyTextRank to the spaCy pipeline
    nlp.add_pipe("textrank", last=True)
    doc = nlp(text)

    prepositions_articles = [
            "ann", "achter", "beneden", "bij", "binnen", "boven", "buiten", "door", "in",
            "langs", "met", "na", "naar", "naast", "om", "onder", "op", "over", "rond", "sinds",
            "te", "tegen", "tegenover", "got", "tussen", "uit", "van", "voor", "zonder",
            "een", "de", "het"
            ]

    regex = re.compile(r'\w+\s')

    keywords = []
    cache = []
    ind = 1
    for p in doc._.phrases:
        k = p.text.lower()
        s = regex.match(k)
        if s:
            matched = s.group(0)
            matched = matched.strip()

            if matched in prepositions_articles:
                span = s.span(0)
                k = k[span[1]:]

        if k not in cache:
            cache.append(k)
            keywords.append((k, p.rank))
            ind += 1

        if ind > top_n:
            break

    return keywords


if __name__ == "__main__":
    keybert_impl('test')
