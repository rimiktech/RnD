import pandas as pd
from name_matching.name_matcher import NameMatcher

print("Reading CSV files..")
lenders_data = pd.read_csv("C:\\Users\\Hp\\Downloads\\lenders.csv")
advertisers_data = pd.read_csv("C:\\Users\\Hp\\Downloads\\advertisers.csv")

matcher = NameMatcher(top_n=10, lowercase=True, punctuations=True, remove_ascii=True, legal_suffixes=False,common_words=False, verbose=True)
matcher.set_distance_metrics(['discounted_levenshtein','SSK', 'fuzzy_wuzzy_token_sort'])

matcher.load_and_process_master_data('lender_name', lenders_data)
matched_data = matcher.match_names(to_be_matched=advertisers_data, column_matching='advertiser_name')

matched_data.to_csv("result.csv")