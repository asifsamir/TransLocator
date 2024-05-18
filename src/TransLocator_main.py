# retrieve top-100 documents for each bug report from elastic search

# first read the bug reports from the json file into the dataframe
# then for each bug report, retrieve the top-100 documents from elastic search
# then save the results into a json file

import pandas as pd

import SearchAspects
from IR.Searcher.Searcher import Searcher
from Utils.IR_Evaluation_Metrics.IR_Performance_Evaluator import Performance_Evaluator


def add_index_to_search_results(search_results):
    for index, search_result in enumerate(search_results):
        search_result["index"] = index + 1

    return search_results


def rerank_DOI(results_dictionary, top_K_results):
    # sort the results based on the ce score
    results_dictionary_cosine = sorted(results_dictionary, key=lambda x: x['score_ce'], reverse=True)

    total_results = len(results_dictionary)

    # calculate the DOI score for each result
    for index, result in enumerate(results_dictionary_cosine):
        doi_score = (total_results - index) / total_results
        result['doi_score_ce'] = doi_score

    # sort the results based on the bm25 score
    results_dictionary_bm25 = sorted(results_dictionary, key=lambda x: x['score_bm25'], reverse=True)

    for index, result in enumerate(results_dictionary_bm25):
        doi_score = (total_results - index) / total_results
        result['doi_score_bm25'] = doi_score

    # combine the two scores
    for index, result in enumerate(results_dictionary):
        result['combined_doi'] = result['doi_score_ce'] + result['doi_score_bm25']

    # sort the results based on the combined score
    results_dictionary = sorted(results_dictionary, key=lambda x: x['combined_doi'], reverse=True)

    return results_dictionary[:top_K_results]


def localize(br_path, kw_model_dir, ce_model_dir, topK_rerank, topN, kw_length):

    bug_reports_df = pd.read_json(br_path)

    keyword_model_path = kw_model_dir
    cross_encoder_model_path = ce_model_dir

    ground_truths_all = []
    search_results_all = []

    searcher = Searcher()

    # iterate over the bug reports and retrieve the top-100 documents from elastic search
    for index, row in bug_reports_df.iterrows():
        bug_id = row["bug_id"]
        project = row["project"]
        sub_project = row["sub_project"]
        version = row["version"]
        ground_truths = row["fixed_files"]

        query = row["bug_title"] + " " + row["bug_description"]
        # search_results = searcher.search(project=project, sub_project=sub_project, version=version, query=query, top_K_results=100)

        search_results = searcher.search_Extended(project=project, sub_project=sub_project, version=version,
                                                  query=query, top_K_results=topK_rerank,
                                                  field_to_return=["file_url", "source_code"])

        # add index to the search results
        search_results = add_index_to_search_results(search_results)

        # first, get the results based on keyword search
        search_results = SearchAspects.SearchKeywords.score_by_keywords(query, search_results, keyword_length=kw_length,
                                                                               model_path=keyword_model_path)

        search_results = SearchAspects.SearchCrossEncoder.score_by_cross_encoder(query, search_results,
                                                                                        ce_model_path=cross_encoder_model_path)

        # now, find the DOI score for each result
        search_results = rerank_DOI(search_results, top_K_results=topN)

        # get only the file urls of the top-10 results as list
        top_10_results = [result["file_url"] for result in search_results[:topN]]

        ground_truths_all.append(ground_truths)
        search_results_all.append(top_10_results)

    performance = Performance_Evaluator.evaluate_several(ground_truths_all, search_results_all, at_Ks=[1, 5, 10])

    return performance


# if __name__ == '__main__':
#     br_path = "D:\Research\Coding\Replication_Package\TransLocator\data\\test_fixed_all_TIMED.json"
#     kw_model_dir = "F:\Models\masked_bugreport_full"
#     ce_model_dir = 'F:\Models\Cross_encoder\CodeBert_Full_DS_Timed'
#     topK_rerank = 100
#     topN = 10
#     length = 10
#     localize(br_path, kw_model_dir, ce_model_dir, topK_rerank, topN, length)
