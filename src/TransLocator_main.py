
# retrieve top-100 documents for each bug report from elastic search

# first read the bug reports from the json file into the dataframe
# then for each bug report, retrieve the top-100 documents from elastic search
# then save the results into a json file

import pandas as pd
from IR.Searcher.Searcher import Searcher
from src import SearchAspects


def add_index_to_search_results(search_results):
    for index, search_result in enumerate(search_results):
        search_result["index"] = index + 1

    return search_results


if __name__ == '__main__':
    # read the bug reports from the json file into the dataframe
    bug_reports_df = pd.read_json("D:\Research\Coding\Replication_Package\TransLocator\data\\test_fixed_all_TIMED.json")

    # print(bug_reports_df.head())

    searcher = Searcher()

    # iterate over the bug reports and retrieve the top-100 documents from elastic search
    for index, row in bug_reports_df.iterrows():
        bug_id = row["bug_id"]
        project = row["project"]
        sub_project = row["sub_project"]
        version = row["version"]
        ground_truths = row["fixed_files"]

        query= row["bug_title"] + " " + row["bug_description"]
        # search_results = searcher.search(project=project, sub_project=sub_project, version=version, query=query, top_K_results=100)

        search_results = searcher.search_Extended(project=project, sub_project=sub_project, version=version, query=query, top_K_results=100, field_to_return=["file_url", "source_code"])

        # add index to the search results
        search_results = add_index_to_search_results(search_results)

        # first, get the results based on keyword search
        re_ranked_keywords = SearchAspects.SearchKeywords.search_by_keywords(query, search_results)
        break