filename = "invoice2go_20375543_client_1712870874166 copy.csv"  
output_filename = "results.csv"

import pandas as pd
import pyap



prepositions = {'-', '@', 'at', 'in', 'of', 'on', 'for', 'with', 'by', 'from', 'to'}

def extract_name(name):
    firstName = ""
    lastName = ""
    companyName = ""

    #Check whether this value is a address.
    if "," in name: return "", "", ""

    #Check whether value has company name also.
    prep = [c for c in name.split(" ") if c.lower() in prepositions]
    if len(prep) > 1: print("Found unexpected value {0}".format(name))
    if len(prep) == 1:
         components = name.split(" " + prep[0] + " ")
         name, companyName = components[0], components[1] if len(components) > 1 else ""
    
    #Check whether value has multiple names.
    prep = [c for c in name.split(" ") if c.lower() in ["and", "&"]]
    if len(prep) > 0: name = name.split(f" {prep[0]} ")[0]

    components = [n for n in name.split(' ') if n.strip() != '']
    if len(components) > 2: #Check whehter it is a name or company name
        companyName = name
        firstName = lastName = ""
    else:
        if len(components) == 1 and "." in components[0]: 
            components = components[0].split(".")
        firstName, lastName = components[0], components[1] if len(components) > 1 else ""
    return firstName, lastName, companyName


def extract_address_components(address):
    address_parser = pyap.parse(address, country="CA") 
    if len(address_parser) > 0:
        parsed_address = address_parser[0]
        street = parsed_address.street_number + " " + parsed_address.street_name if parsed_address.street_name is not None else ""
        city = parsed_address.city
        province = parsed_address.region1
        return street, city, province
    return "", "", ""



if __name__ == "__main__":
    data = pd.read_csv(filename)
    data['first name'], data['last name'], data['company'] = zip(*data['BillingName'].fillna("").map(extract_name))
    data['address'], data['city'], data['province'] = zip(*data['BillingAddress'].fillna("").map(extract_address_components))
    result = data[["first name", "last name", "company", "address", "city", "province"]]
    result.to_csv(output_filename, index=False)