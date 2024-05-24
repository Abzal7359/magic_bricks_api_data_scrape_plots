import requests
import csv
import re


def fetch_properties(page, offset):
    url = "https://www.magicbricks.com/mbsrp/propertySearch.html"
    params = {
        "editSearch": "Y",
        "category": "S",
        "propertyType": "10000",
        "city": "2060",
        "page": page,
        "groupstart": offset,
        "offset": 0,
        "maxOffset": 38,
        "sortBy": "premiumRecent",
        "postedSince": -1,
        "pType": "10000",
        "areaUnit": 12850,
        "isNRI": "N",
        "multiLang": "en"
    }
    response = requests.get(url, params=params)
    print(f"Fetching page {page} with offset {offset}, Status Code: {response.status_code}")
    response.raise_for_status()
    return response.json()


def extract_dimensions(seo_desc):
    match = re.search(r'(\d+(\.\d+)?)\s*X\s*(\d+(\.\d+)?)', seo_desc)
    if match:
        return match.group(0)  # Return the full matched dimensions string
    return ''


def extract_data(property_data):
    fields = ["url", "prjname", "devName", "price", "priceD", "sqFtPrD", "reraId", "propTypeD", "lmtDName",
              "waterStatus", "postDateT"]
    extracted = {field: property_data.get(field, '') for field in fields}

    seo_desc = property_data.get('seoDesc', '')
    extracted['dimensions'] = extract_dimensions(seo_desc)

    return extracted


def write_to_csv(data, filename='properties1.csv'):
    fields = ["url", "prjname", "devName", "price", "priceD", "sqFtPrD", "reraId", "propTypeD", "lmtDName",
              "waterStatus", "postDateT", "dimensions"]
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(data)


# Fetch and process data
all_properties = []
page = 1
offset = 0
max_pages = 2  # Limit to 30 pages

for page in range(1, max_pages + 1):
    json_data = fetch_properties(page, offset)
    result_list = json_data.get('resultList', [])

    print(f"Number of properties fetched on page {page}: {len(result_list)}")

    for prop in result_list:
        extracted = extract_data(prop)
        all_properties.append(extracted)
        print(f"Extracted property: {extracted}")

    offset += 30  # Increment offset by 30 for the next page

print(f"Total properties fetched: {len(all_properties)}")
write_to_csv(all_properties)
print("Data written to CSV file successfully.")

#--------------------------------------------------------------------------------------------------------------------------
# import requests
# import csv
#
#
# def fetch_properties(page, offset):
#     url = "https://www.magicbricks.com/mbsrp/propertySearch.html"
#     params = {
#         "editSearch": "Y",
#         "category": "S",
#         "propertyType": "10000",
#         "city": "2060",
#         "page": page,
#         "groupstart": offset,
#         "offset": 0,
#         "maxOffset": 38,
#         "sortBy": "premiumRecent",
#         "postedSince": -1,
#         "pType": "10000",
#         "areaUnit": 12850,
#         "isNRI": "N",
#         "multiLang": "en"
#     }
#     response = requests.get(url, params=params)
#     print(f"Fetching page {page} with offset {offset}, Status Code: {response.status_code}")
#     response.raise_for_status()
#     return response.json()
#
#
# def extract_data(property_data):
#     fields = ["url", "prjname", "devName", "price", "priceD", "sqFtPrD", "reraId", "propTypeD", "lmtDName",
#               "waterStatus", "postDateT"]
#     extracted = {field: property_data.get(field, '') for field in fields}
#     return extracted
#
#
# def write_to_csv(data, filename='properties.csv'):
#     fields = ["url", "prjname", "devName", "price", "priceD", "sqFtPrD", "reraId", "propTypeD", "lmtDName",
#               "waterStatus", "postDateT"]
#     with open(filename, mode='w', newline='', encoding='utf-8') as file:
#         writer = csv.DictWriter(file, fieldnames=fields)
#         writer.writeheader()
#         writer.writerows(data)
#
#
# # Fetch and process data
# all_properties = []
# page = 1
# offset = 0
# max_pages = 2  # Limit to 30 pages
#
# for page in range(1, max_pages + 1):
#     json_data = fetch_properties(page, offset)
#     result_list = json_data.get('resultList', [])
#
#     print(f"Number of properties fetched on page {page}: {len(result_list)}")
#
#     for prop in result_list:
#         extracted = extract_data(prop)
#         all_properties.append(extracted)
#         print(f"Extracted property: {extracted}")
#
#     offset += 30  # Increment offset by 30 for the next page
#
# print(f"Total properties fetched: {len(all_properties)}")
# write_to_csv(all_properties)
# print("Data written to CSV file successfully.")
