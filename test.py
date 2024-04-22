import string
import pandas as pd

def normalize(names):
    names = names.str.lower()
    names = names.str.replace('[{}]'.format(string.punctuation), '', regex=True)

    words_to_remove = ['llc', 'inc', 'co', 'corp', 'company', 'bank', 'limited', 'ltd', 'group', 
                       'holdings', 'partners', 'associates', 'services', 'enterprises', 'international', 
                       'int', 'plc', 'na']
    for word in words_to_remove:
        names = names.str.replace(r'\b{}\b'.format(word), '', regex=True)
    names = names.str.strip()
    return names


lenders_data = pd.read_csv("C:\\Users\\Hp\\Downloads\\lenders.csv")
lenders_data = lenders_data.drop_duplicates(subset='lender_name')
lenders_data['normalized_lender_name'] = normalize(lenders_data['lender_name'])
#lenders_data = lenders_data.drop_duplicates(subset='normalized_lender_name')


advertisers_data = pd.read_csv("C:\\Users\\Hp\\Downloads\\advertisers.csv")
advertisers_data = advertisers_data.drop_duplicates(subset='advertiser_name')
advertisers_data['normalized_advertiser_name'] = normalize(advertisers_data['advertiser_name'])
#advertisers_data = advertisers_data.drop_duplicates(subset='normalized_advertiser_name')

#common_names = pd.merge(lenders_data, advertisers_data, left_on='normalized_lender_name', right_on='normalized_advertiser_name', how='inner')
import pdb
pdb.set_trace()
