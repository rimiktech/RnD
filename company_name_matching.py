import string
import pandas as pd
from name_matching.name_matcher import NameMatcher

def normalize(names):
    names = names.str.lower()
    names = names.str.replace('[{}]'.format(string.punctuation), '', regex=True)

    words_to_remove = ['llc', 'inc', 'co', 'corp', 'company', 'bank', 'limited', 'ltd', 'group', 'holdings', 'partners', 'associates', 
                       'services', 'enterprises', 'international', 'int', 'plc', 'na', 'the', 'n a', 'bancorp']
    for word in words_to_remove:
        names = names.str.replace(r'\b{}\b'.format(word), '', regex=True)
    names = names.str.strip()
    return names

print("Reading lenders data")
lenders_data = pd.read_csv("lenders.csv")
print("Normalizing lenders name")
lenders_data['normalized_lender_name'] = normalize(lenders_data['lender_name'])
print("Droping duplicates lenders name")
lenders_data = lenders_data.drop_duplicates(subset='normalized_lender_name')


print("Reading advertisers data")
advertisers_data = pd.read_csv("advertisers.csv")
print("Normalizing advertisers name")
advertisers_data['normalized_advertiser_name'] = normalize(advertisers_data['advertiser_name'])
print("Droping duplicate advertisers name")
advertisers_data = advertisers_data.drop_duplicates(subset='normalized_advertiser_name')

matcher = NameMatcher(top_n=10, lowercase=True, punctuations=True, remove_ascii=True, legal_suffixes=False,common_words=False, verbose=True)
matcher.set_distance_metrics(['discounted_levenshtein','SSK', 'fuzzy_wuzzy_token_sort'])
matcher.load_and_process_master_data('normalized_advertiser_name', advertisers_data)
matched_data = matcher.match_names(to_be_matched=lenders_data, column_matching='normalized_lender_name')
matched_data = matched_data[matched_data['score']>=80]
matched_data = matched_data.drop_duplicates(subset='original_name')

combined = pd.merge(advertisers_data, matched_data, how='outer', left_index=True, right_on='match_index')
combined = pd.merge(combined, lenders_data, how='outer', left_index=True, right_index=True)

combined.drop(columns=['year_x', 'normalized_advertiser_name', 'original_name', 'match_name', 'year_y', 'normalized_lender_name'], inplace=True)
combined.reset_index(drop=True, inplace=True)
combined = combined[['lender_name', 'lender_id', 'advertiser_name', 'advertiser_id', 'match_index', 'score']]
combined.to_csv("combined_data.csv")


