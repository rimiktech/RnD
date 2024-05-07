import string
import numpy as np
import pandas as pd
from name_matching.name_matcher import NameMatcher

file1 = "./data/lenders (2).csv"
file2 = "./data/advertisers (2).csv"
output = "adv_lender_data.csv"

words_to_replace = {
    'llc': 'limited liability company', 'inclave': 'inc', 'Incorporat': 'inc', 'co': 'company',
    'corp': 'corporation', 'ltd': 'limited', 'grp': 'group', 'int': 'international', 'intl': 'international',
    'plc': 'public limited company', '1st': 'first', 'ntl': 'national', 'nb': 'national bank', 'bk': 'bank',
    'b&tc': 'bank and trust company', '&': 'and', 'bkg': 'banking', 'mortg': 'mortgage', 'cap': 'capital',
    'org': 'organization', 'mtg': 'mortgage',

    'holdings': '', 'hold': '', 'hldgs': '', 'partners': '', 'associates': '', 'services': '', 'enterprises': '', 
    'na': '', 'the': '', 'n a': '', 'bancorp': '', 'of': ''
}


def normalize(names):
    names = names.str.lower()
    names = names.str.replace('[{}]'.format(string.punctuation), '', regex=True)
    for word, value in words_to_replace.items():
        names = names.str.replace(r'\b{}\b'.format(word), value, regex=True)
    names = names.str.strip()
    return names

print("Reading lenders data")
lenders_data = pd.read_csv(file1)

print("Droping duplicates lenders name")
lenders_data['respondentname'].str.lower()
lenders_data = lenders_data.drop_duplicates(subset='respondentname')

print("Normalizing lenders name")
pattern = r'^\d+-\d+$'
lenders_data['parentname'] = lenders_data['parentname'].mask(pd.to_numeric(lenders_data['parentname'], errors='coerce').notna())
lenders_data['parentname'] = lenders_data.loc[lenders_data['parentname'].astype(str).str.match(pattern), 'parentname'] = np.nan
missing_lenders_parent = lenders_data['parentname'].isnull()
lenders_data.loc[missing_lenders_parent, 'parentname'] = lenders_data.loc[missing_lenders_parent, 'respondentname']
lenders_data['normalized_lender_name'] = normalize(lenders_data['parentname'])
lenders_data = lenders_data.drop_duplicates(subset = 'normalized_lender_name')


print("Reading advertisers data")
advertisers_data = pd.read_csv(file2)

print("Droping duplicate advertisers name")
advertisers_data['advertiser'].str.lower()
advertisers_data = advertisers_data.drop_duplicates(subset='advertiser')

print("Normalizing advertisers name")
advertisers_data['parent'] = advertisers_data['parent'].fillna('PARENT UNKNOWN')
missing_advertisers_parent = advertisers_data['parent'].isnull()
advertisers_data.loc[missing_advertisers_parent, 'parent'] = advertisers_data.loc[missing_advertisers_parent, 'advertiser']
advertisers_data['normalized_advertiser_name'] = normalize(advertisers_data['parent'])
advertisers_data = advertisers_data.drop_duplicates(subset ='normalized_advertiser_name')

matcher = NameMatcher(top_n=10, lowercase=True, punctuations=True, remove_ascii=True, legal_suffixes=False,common_words=False, verbose=True)
matcher.set_distance_metrics(['discounted_levenshtein','SSK', 'fuzzy_wuzzy_token_sort'])
matcher.load_and_process_master_data('normalized_advertiser_name', advertisers_data)

matched_data = matcher.match_names(to_be_matched=lenders_data, column_matching='normalized_lender_name')
matched_data = matched_data[matched_data['score'] >= 80]
matched_data = matched_data.drop_duplicates(subset='original_name')
print("{0} Matched rows found whose score is above 80".format(len(matched_data)))

print("Merging dataframes")
combined = pd.merge(advertisers_data, matched_data, how='outer', left_index=True, right_on='match_index')
combined = pd.merge(combined, lenders_data, how='outer', left_index=True, right_index=True)

print("Droping extra columns")
combined = combined[['respondentname', 'parentname', 'hmda_id', 'advertiser', 'parent', 'advertiser_id', 'score']]

print("Saving merged data into CSV file")
combined.to_csv(output)