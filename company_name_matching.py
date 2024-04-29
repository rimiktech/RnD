import string
import pandas as pd
from name_matching.name_matcher import NameMatcher

words_to_remove = [
    'llc', 'inc', 'co', 'corp', 'company', 'bank', 'limited', 'ltd', 'group', 'holdings', 'partners', 'associates', 
    'services', 'enterprises', 'international', 'int', 'plc', 'na', 'the', 'n a', 'bancorp', 
    'national', 'plc', 'corporate', 'mortage', 'mortgage', 'financial', 'of', 'and', '&', 
]

#'first', '1st', 'ist'

def normalize(names):
    names = names.str.lower()
    names = names.str.replace('[{}]'.format(string.punctuation), '', regex=True)
    for word in words_to_remove:
        names = names.str.replace(r'\b{}\b'.format(word), '', regex=True)
    names = names.str.strip()
    return names

print("Reading lenders data")
lenders_data = pd.read_csv("./data/lenders (1).csv")
print("Normalizing lenders name")
lenders_data['normalized_lender_name'] = normalize(lenders_data['respondentname'])
print("Droping duplicates lenders name")
lenders_data = lenders_data.drop_duplicates(subset='normalized_lender_name')


print("Reading advertisers data")
advertisers_data = pd.read_csv("./data/advertisers (1).csv")
print("Normalizing advertisers name")
advertisers_data['normalized_advertiser_name'] = normalize(advertisers_data['advertiser_name'])
print("Droping duplicate advertisers name")
advertisers_data = advertisers_data.drop_duplicates(subset='normalized_advertiser_name')

matcher = NameMatcher(top_n=10, lowercase=True, punctuations=True, remove_ascii=True, legal_suffixes=False,common_words=False, verbose=True)
matcher.set_distance_metrics(['discounted_levenshtein','SSK', 'fuzzy_wuzzy_token_sort'])
matcher.load_and_process_master_data('normalized_advertiser_name', advertisers_data)

matched_data = matcher.match_names(to_be_matched=lenders_data, column_matching='normalized_lender_name')
matched_data = matched_data[matched_data['score'] >= 50]
matched_data = matched_data.drop_duplicates(subset='original_name')
print("{0} Matched rows found whose score is above 80".format(len(matched_data)))

print("Merging dataframes")
combined = pd.merge(advertisers_data, matched_data, how='outer', left_index=True, right_on='match_index')
combined = pd.merge(combined, lenders_data, how='outer', left_index=True, right_index=True)

print("Droping extra columns")
combined = combined[['respondentname', 'hmda_id', 'advertiser_name', 'advertiser_id', 'score']]

print("Saving merged data into CSV file")
combined.to_csv("adv_lender_data.csv")