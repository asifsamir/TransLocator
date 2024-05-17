from flair.embeddings import TransformerDocumentEmbeddings
from keybert import KeyBERT
from rank_bm25 import BM25Okapi, BM25L

from src.Utils import TextPreprocessor


def find_keywords(query, keyword_length, model_path):
    # model_path = "F:\Models\masked_bugreport_full"
    model = TransformerDocumentEmbeddings(model_path=model_path)
    kw_model = KeyBERT(model=model)

    keywords = kw_model.extract_keywords(query, keyphrase_ngram_range=(3, 4), stop_words='english', top_n=keyword_length, use_mmr=True, diversity=0.7)

    return keywords


def score_search_results(search_results_es, keywords):

    text_preprocessor = TextPreprocessor()

    # merge the keywords into a single string
    query = " ".join(keywords)

    # tokenize the query
    query = query.split(" ")

    corpus = [search_result["source_code"] for search_result in search_results_es]

    # tokenize the corpus
    for index, doc in enumerate(corpus):
        corpus[index] = text_preprocessor.preprocess(doc)


    # create the bm25 object
    bm_25 = BM25L(corpus)

    # get the scores
    scores = bm_25.get_scores(query)

    # iterate over the search results and add the scores to the search results
    for index, search_result in enumerate(search_results_es):
        search_result["score_bm25"] = scores[index]

    return search_results_es



def score_by_keywords(query, search_results_es, keyword_length, model_path):

    # find keywords first
    keywords = find_keywords(query, keyword_length, model_path=model_path)
    # keywords are list of tuples, convert them to a list of strings taking the first element of the tuple
    keywords = [keyword[0] for keyword in keywords]

    # now using the keywords, find the bm25 scores of the search results
    score_docs = score_search_results(search_results_es, keywords)

    # sort the search results based on the bm25 scores
    # score_docs = sorted(score_docs, key=lambda x: x["score_bm25"], reverse=True)

    return score_docs


if __name__ == '__main__':
    query = '''From version 1.5 and onwards the CachingConnectionFactory will not allow any connections to be created once the application context has been closed. This is implemented by closing the connection factory as soon as closing of the application context is initiated (when the ContextClosedEvent is fired).
This is quite abrupt and causes problems for code that may want to process requests and publish messages while the application context is still in it&apos;s closing stage.
As an example we use spring-integration AMQP components (AmqpInboundChannelAdapter) for consuming inbound messages and these components implement the Spring SmartLifeCycle. This means that message consumers are not stopped until you reach the life-cycle processing stage in the application context closing (which happens after the ContextClosedEvent is fired). This causes problems as you cannot easily prevent incoming messages from arriving but you cannot send any outbound messages (since the connection factory is already closed). 
For us this is major issue since it now limits our possibility to perform a graceful shutdown of our application, which worked well with prior versions.
If closing is really required then I think it could make sense to defer it to a later stage by e.g. implementing Spring SmartLifeCycle and use the stop() method. Combined with a configurable phase that would give us the possibility to co-ordinate the closing with other components that should be stopped before we let the application context start destroying beans.'''
    search_results_es = [{'source_code': '''public class CachingConnectionFactory extends SingleConnectionFactory implements SmartLifecycle, DisposableBean {}
    public void onApplicationEvent(ContextClosedEvent event) {
        if (event.getApplicationContext() == this.applicationContext) {
            stop();
        }
    }'''}]
    keyword_length = 5

    print(score_by_keywords(query, search_results_es, keyword_length))

