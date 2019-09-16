import json
import requests
import requests_oauthlib
import sqlite3
import csv
from requests_oauthlib import OAuth1


# Connects to 'icomProducts' sqlite3 database
conn = sqlite3.connect('icomProducts.db')

# Sets cursor
cursor = conn.cursor()

# WooCommerce STAGING Consumer Key
key = 'ck_5b1aedb5d3990bf8c508c5b1343662290aaac104'
# Woo Commerce STAGING Consumer Secret
secret = 'cs_6a7f393d186f42d569a1a5c31d3747464f3bba32'

# WooCommerce active site key and secret
# 'ck_acdaf69d09e0281ab2ae925c5da91319475e15eb'
# 'cs_4ab044b43f43b234f93e775176f36553ff68cc3b'

accessory_categories = [{'id': 101, 'name': 'Accessories'}, {'id': 109, 'name':'Antenna Switches'}, {'id': 90, 'name':'Antenna Tuners'},
                        {'id': 89, 'name': 'Antennas'}, {'id': 93, 'name': 'Batteries'}, {'id': 92, 'name': 'Belt Clips'},
                        {'id': 115, 'name': 'Cabinets'},{'id': 103, 'name': 'Cables'}, {'id': 91, 'name': 'Carrying Cases'},
                        {'id': 88, 'name': 'Chargers'},{'id': 99, 'name': 'Configurations'},{'id': 112, 'name': 'Duplexers'},
                        {'id': 97, 'name': 'Encryption & Internal Modules'},{'id': 120, 'name': 'External Speakers'},
                        {'id': 119, 'name': 'Filters'},{'id': 108, 'name': 'GPS'},
                        {'id': 107, 'name': 'Headsets'}, {'id': 94, 'name': 'IP Linking'}, {'id': 117, 'name': 'Licenses'},
                        {'id': 100, 'name': 'Microphones'},{'id': 87, 'name': 'Miscellaneous'},
                        {'id': 102, 'name': 'Mounting Hardware'}, {'id': 118, 'name': 'Pilot Tone Generator'},{'id': 113, 'name': 'Power Amplifiers'},
                        {'id': 111, 'name': 'Power Equipment & Rack Mounting'}, {'id': 95, 'name': 'Power Supplies'},
                        {'id': 116, 'name': 'Pre-Selectors'},{'id': 114, 'name': 'Racks'},{'id': 110, 'name': 'RedHawk'},
                        {'id': 98, 'name': 'Remote Communication'}, {'id': 106, 'name': 'Remote Mounting'}, {'id': 121, 'name': 'Repeaters'},{'id': 96, 'name': 'Software & Cables'},
                        {'id': 104, 'name': 'Trunking'}, {'id': 86, 'name': 'Trunking/Network Controller'},{'id': 105, 'name': 'Wire Kits'}]

accessory_tags = [{'id':182, 'name': 'F1000D - F2000D Series'}, {'id':183, 'name': 'F1000ST - F2000ST Series'},{'id':184, 'name': 'F1100D - F2100D Series'},
                  {'id':185, 'name': 'F3001 - F4001 Series'},{'id':186, 'name': 'F3011 - F4011 Series'},{'id':187, 'name': 'F3161 - F4161 & F3161D - F4161D Series'},
                  {'id':188, 'name': 'F3201DEX - F4201DEX Series'},{'id':189, 'name': 'F3210D - F4210D Series'},{'id':190, 'name': 'F3230D - F4230D Series'},{'id':191, 'name':'F3261D - F4261D Series'},
                  {'id':192, 'name': 'F3360D - F4360D Series'},{'id':193, 'name': 'F3400D - F4400D Series'},{'id':194, 'name': 'F52D - F62D Series'},{'id':195, 'name': 'F70 - F80 - F70D - F80D Series'},
                  {'id':196, 'name':'F7010 - F7020 Series'},{'id':197, 'name': 'F9011 - F9021 Series'},{'id':198, 'name': 'CY5000 - CY6000 Repeaters'},{'id':199, 'name': 'F5011 - F6011 Series'},
                  {'id':200, 'name': 'F5021 - F6021 Series'},{'id':201, 'name': 'F5061 - F6061 & F5061D - F6061D Series'},{'id':202, 'name': 'F5121D - F6121D Series'},
                  {'id':203, 'name': 'F5220D - F6220D Series'},{'id':204, 'name': 'F5360D - F6360D Series'},{'id':205, 'name': 'F5400D - F6400D Series'},{'id':206, 'name': 'F7510 - F7520 Series'},
                  {'id':207, 'name': 'F8101'},{'id':208, 'name': 'F9511 - F9521 Series'},{'id':209, 'name': 'IAS 120D - 150D Series'},{'id':210, 'name': 'VE-PG3'},{'id':211, 'name': 'X-BAND REPEATER'},
                  {'id':212, 'name':'F1721 - F2721 - F2821 Series'},{'id':213, 'name': 'FR5000 - FR6000 Series'},{'id':214, 'name': 'FR5200H - FR6200H Series'},
                  {'id':215, 'name': 'FR9010 - FR9020 Series'},{'id':216, 'name': 'RF Technologies - Eclipse2 Series'},{'id':217, 'name':'F50V/F60V Series (Discontinued)'},
                  {'id':218, 'name': 'F3031S - F4031S Series (Discontinued)'},{'id':219, 'name': 'F11-F21 (Discontinued)'},{'id':220, 'name': 'F14/F24 - F33G/F43G - F43TR - F3021/F4021 (Discontinued)'},
                  {'id':221, 'name':'F30G - F40G Series (Discontinued)'}]

radio_categories = [{'id': 123, 'name': 'Mobiles'},{'id': 122, 'name': 'Portables'},{'id': 124, 'name': 'Data Radio, HF, & RoIPSolutions'},{'id': 125, 'name': 'Icom America Systems'}]

radio_tags = [{'id': 91, 'name': 'Hospitality'},{'id': 92, 'name': 'Law Enforcement'},{'id': 93, 'name': 'Manufacturing'},{'id': 94, 'name': 'Oil & Gas'},
            {'id': 95, 'name': 'Public Safety'},{'id': 96, 'name': 'Retail'},{'id': 97, 'name': 'Transportation & Logistics'},{'id': 98, 'name': 'Utilities'},
            {'id': 99, 'name': 'Construction'},{'id': 100, 'name': 'Education'}, {'id': 101, 'name': 'Fire & EMS'},{'id': 102, 'name': 'Healthcare'}]

accessory_cat_list = ['Trunking/Network Controller', 'Miscellaneous', 'Chargers', 'Antennas', 'Antenna Tuners', 'Carrying Cases', 'Belt Clips', 'Batteries', 'IP Linking', 'Power Supplies',
            'Software & Cables', 'Encryption & Internal Modules', 'Remote Communication', 'Configurations', 'Microphones', 'Accessories', 'Mounting Hardware', 'Cables',
            'Trunking', 'Wire Kits', 'Remote Mounting', 'Headsets', 'GPS', 'Antenna Switches', 'RedHawk', 'Power Equipment & Rack Mounting', 'Duplexers', 'Power Amplifiers',
            'Racks', 'Cabinets', 'Pre-Selectors', 'Licenses', 'Pilot Tone Generator', 'Filters', 'External Speakers', 'Repeaters']

radio_cat_list = ['Portables', 'Mobiles', 'Data Radio, HF, & RoIPSolutions', 'Icom America Systems']


def create_parent_cat():

    cats = ['Radios', 'Accessories']
    for cat in cats:

        data = {"name": cat}

        headers = {"Content-Type": "application/json", "wp_api": "True", "version": "wc/v3"}

        req = requests.post('http://staging.gotoess.flywheelsites.com/wp-json/wc/v3/products/categories',
                            auth=OAuth1(client_key=key, client_secret=secret), headers=headers, data=json.dumps(data))

        print(req)

# create_parent_cat()


# Creates WooCommerce category
def create_sub_cats():

    # creates sub categories under Accessories parent category (id: 30)
    for cat in radio_cat_list:

        data = {
            "name": cat,
            "parent": 84
        }

        headers = {"Content-Type": "application/json", "wp_api": "True", "version": "wc/v3"}

        req = requests.post('http://staging.gotoess.flywheelsites.com/wp-json/wc/v3/products/categories',
                            auth=OAuth1(client_key=key, client_secret=secret), headers=headers, data=json.dumps(data))

        print(req.json())


# create_sub_cats()

def create_tag():

    tags = ['F1000D - F2000D Series','F1000ST - F2000ST Series','F1100D - F2100D Series','F3001 - F4001 Series','F3011 - F4011 Series',
            'F3161 - F4161 & F3161D - F4161D Series','F3201DEX - F4201DEX Series','F3210D - F4210D Series','F3230D - F4230D Series',
            'F3261D - F4261D Series','F3360D - F4360D Series','F3400D - F4400D Series','F52D - F62D Series','F70 - F80 - F70D - F80D Series',
            'F7010 - F7020 Series','F9011 - F9021 Series','CY5000 - CY6000 Repeaters','F5011 - F6011 Series','F5021 - F6021 Series',
            'F5061 - F6061 & F5061D - F6061D Series','F5121D - F6121D Series','F5220D - F6220D Series','F5360D - F6360D Series',
            'F5400D - F6400D Series','F7510 - F7520 Series','F8101','F9511 - F9521 Series','IAS 120D - 150D Series','VE-PG3','X-BAND REPEATER',
            'F1721 - F2721 - F2821 Series','FR5000 - FR6000 Series','FR5200H - FR6200H Series','FR9010 - FR9020 Series','RF Technologies - Eclipse2 Series',
            'F50V/F60V Series (Discontinued)','F3031S – F4031S Series (Discontinued)','F11-F21 (Discontinued)','F14/F24 - F33G/F43G - F43TR – F3021/F4021 (Discontinued)',
            'F30G – F40G Series (Discontinued)']

    for tag in tags:

        data = {
            "name": tag
        }

        headers = {"Content-Type": "application/json", "wp_api": "True", "version": "wc/v3"}

        req = requests.post('http://staging.gotoess.flywheelsites.com/wp-json/wc/v3/products/tags',
                            auth=OAuth1(client_key=key, client_secret=secret), headers=headers, data=json.dumps(data))

        print(req.json())


# create_tag()

def post_accessory():

    for num, row in enumerate(cursor.execute("SELECT * FROM accessories"), start = 1):
        if num > 0:
            sku = row[0]
            name = row[1]
            description = row[2]
            price = row[3]
            tags = row[4].replace("[", "").replace("]", "").replace("'", "").split(", ")
            cats = row[5]

            # try:
            #     s3_urls = row[8].decode('utf-8').replace("[", "").replace("]", "").replace("'", "").split(", ")
            # except:
            #     s3_urls = row[8].replace("[", "").replace("]", "").replace("'", "").split(", ")

             # sub_cats = row[4].split(", ")

            try:
                cats_list = []
                for item in range(0, len(accessory_categories)):
                    if cats == accessory_categories[item]['name']:
                        cat_id = accessory_categories[item]['id']
                        cat_name = accessory_categories[item]['name']
                        cats_list.append({"id": cat_id, 'name': cat_name})
            except:
                cats_list = []

            try:
                tags_list = []

                for tag in tags:
                    for item in range(0, len(accessory_tags)):
                            id = accessory_tags[item]['id']
                            if tag == accessory_tags[item]['name']:
                                tag_id = accessory_tags[item]['id']
                                tag_name = accessory_tags[item]['name']
                                tags_list.append({"id": tag_id, 'name': tag_name})
            except:
                 tags_list = []
            tags_list.append({"id": 222, 'name': 'icom'})

            # images = []
            # for img in s3_urls:
            #     if img == 'http://cybercomm.flywheelsites.com/wp-content/uploads/2019/07/img_notavailable_insignia-01.png':
            #         images = []
            #     else:
            #         images.append({"src": img})

            # if float(price) > 499.99 or float(price) == 0.0:
            data = {
                "name": name,
                "type": "simple",
                "sku": sku,
                "regular_price": str(price),
                "short_description": sku,
                "description": description,
                "categories": cats_list,
                "tags": tags_list,
                "meta_data": [
                    {
                        'key': 'is_quotable',
                        'value': False
                    }
                ]
            }

            # else:
            #     data = {
            #         "name": name,
            #         "type": "simple",
            #         "sku": sku,
            #         "regular_price": str(price),
            #         "short_description": info,
            #         "description": description,
            #         "categories": cats_list,
            #         "tags": tags_list,
            #         "images": images,
            #     }
            #
            # print(sku, data)

            headers = {"Content-Type": "application/json", "wp_api": "True", "version": "wc/v3"}
            req = requests.post('http://staging.gotoess.flywheelsites.com/wp-json/wc/v3/products',
                            auth=OAuth1(client_key=key, client_secret=secret), headers=headers,
                            data=json.dumps(data))
            print(num, req.json())

# post_accessory()

def post_radios():

    for row in cursor.execute("SELECT * FROM radios"):

        name = row[0]
        description = row[1]
        specs = row[2]
        features = row[3]
        category = row[4]
        brochures = row[6]

        # cats = row[2].replace("[", "").replace("]", "").replace("'", "").split(", ")
        # tags = row[3].replace("[", "").replace("]", "").replace("'", "").split(", ")

        try:
            s3_urls = row[5].decode('utf-8').replace("[", "").replace("]", "").replace("'", "").split(", ")
        except:
            s3_urls = row[5].replace("[", "").replace("]", "").replace("'", "").split(", ")
        s3_urls = s3_urls[0].split(',')

        cats_list = []

        for item in range(0, len(radio_categories)):
            if category == radio_categories[item]['name']:
                cat_id = radio_categories[item]['id']
                cat_name = radio_categories[item]['name']
                cats_list.append({"id": cat_id, 'name': cat_name})

        tags_list = []
        for item in range(0, len(accessory_tags)):
            try:
                if name == accessory_tags[item]['name']:
                    tag_id = accessory_tags[item]['id']
                    tag_name = accessory_tags[item]['name']
                    tags_list.append({"id": tag_id})
            except:
                tags_list = []
        tags_list.append({"id": 222, 'name': 'icom'})

        images = []
        for img in s3_urls:
            if img == '':
                images = []
            else:
                images.append({"src": img})
        # print(images)

        # productName, description, categories, tags, industry, features, professional_commercial, radioShortname, S3images
        data = {
            "name": name,
            "type": "simple",
            "description": description,
            "specifications": specs,
            "features": features,
            "categories": cats_list,
            "tags": tags_list,
            "images": images,
            "meta_data": [
                {
                    'key': 'is_quotable',
                    'value': True
                },
                {
                    'key': 'specifications',
                    'value': specs
                }
            ]
        }

        headers = {"Content-Type": "application/json", "wp_api": "True", "version": "wc/v3"}
        req = requests.post('c',
                            auth=OAuth1(client_key=key, client_secret=secret), headers=headers,
                            data=json.dumps(data))
        print(req.json())

post_radios()

def get_products():

    headers = {"Content-Type": "application/json", "wp_api": "True", "version": "wc/v3"}
    req = requests.get('http://staging.gotoess.flywheelsites.com/wp-json/wc/v3/products',
                        auth=OAuth1(client_key=key, client_secret=secret), headers=headers)

    response = json.loads(req.text)

    product_list = []

    for product in response:
        product_list.append(product['id'])

    return product_list

# get_products()