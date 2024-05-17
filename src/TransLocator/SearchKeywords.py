import keybert

def search_by_keywords(keywords, top_K_results=10):
    model = keybert.KeyBERT('distilbert-base-nli-mean-tokens')
    search_results = model.extract_keywords(keywords, keyphrase_ngram_range=(1, 1), stop_words='english', top_n=top_K_results)
    return search_results