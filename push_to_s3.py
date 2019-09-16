import urllib.request
import sqlite3
import json
import pathlib
import boto3
import csv
import time
import random
import logging
import os

# open logging file
import dictionary as dictionary

# Amazon S3 Access Key
access_key = 'AKIAIWJPDKSV2YTGL5RA'

# Amazon S3 Secret Key
secret_key = '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'

# connect with Boto3 and start session
session = boto3.Session(
   aws_access_key_id=access_key,
   aws_secret_access_key=secret_key,
)

s3 = session.resource('s3')

# Creates Bucket in Amazon S3 account
def create_bucket(bucketname):
    s3.create_bucket(Bucket=bucketname, CreateBucketConfiguration={'LocationConstraint': 'us-east-2'})

# create_bucket('icom-radio-images')


# Creates file in specified Amazon S3 Bucket
def create_file(bucketname, savename, filename):
    s3.Object(bucketname, savename).put(Body=open(filename, 'rb'))



def write_to_csv(category, prod_name, image_list):
    with open('icom-radios2.csv', 'a+', encoding='utf-8', newline='') as f:
        w = csv.writer(f)
        prod_name = prod_name.replace(' ','+')

        for image in image_list:
            object_url = f'https://icom-radio-images.s3.us-east-2.amazonaws.com/{category}/{prod_name}/{image}'
            w.writerow(object_url)




def write_to_s3():
    rootdir = 'C:\\Users\\obo\\PycharmProjects\\ESSOL\\images\\images_being_used'
    image_paths = []
    counter = 0

    for num, files in enumerate(os.walk(rootdir)):
        if num > 0:
            rootdir = files[0]
            for file in files[2]:
                dir_path = os.path.abspath(os.path.join(rootdir, file))
                dir_path.replace('\\', '\\\\')
                image_paths.append(dir_path)
    # print(image_paths)

    with open('icom-radios.csv', 'r', encoding='utf-8') as f:
        r = csv.reader(f)
        next(f)

        for row in r:
            prod_name = row[0]
            category = row[4]
            image_list = []
            counter += 1
            for image in image_paths:
                if prod_name in image:
                    image_name = image.split('\\')[8]
                    image_list.append(image_name)
                    print(image_name)
                    try:
                        create_file('icom-radio-images', f'{category}/{prod_name}/{image_name}', image)
                        print(image)
                    except:
                        print(f'{image} already exists')
            # write_to_csv(category, prod_name, image_list)
write_to_s3()

def old_write_to_s3():
    count = 0

    with open('icom-radios.csv', 'r', encoding='utf-8') as f:
        r = csv.reader(f)
        next(f)

        for row in r:
            prod_name = row[0]
            category = row[4]
            image_name = row[1]

            if image_name != ['']:

                for number, img in enumerate(image_name, start=1):

                    # write images to s3
                    if type == 'jpg':
                        create_file('moto-radio-images',
                                    f'{category}/{prod_name}/{prod_name}_{str(number)}.jpg',
                                    f'C:\\Users\\obo\\PycharmProjects\\CYCOM\\radio_images\\{category}\\{img}.jpg')

                    elif type == 'png':
                        create_file('moto-radio-images',
                                    f'{category}/{prod_name}/{prod_name}_{str(number)}.png',
                                    f'C:\\Users\\obo\\PycharmProjects\\CYCOM\\radio_images\\{category}\\{img}.png')

                    count += 1
                    print(count)

# old_write_to_s3()


def save_s3_urls():

    url_list = []

    # open and loop thru .csv file containing radios
    with open('accessories.csv', 'r', encoding='utf8') as f:
        r = csv.reader(f)
        next(f)

        for num,row in enumerate(r, start=1):
            if num > 1:
                prod_id = row[0].replace(' ','')
                category = row[6].replace(' ','')
                image_name = row[8].split(',')

                if image_name != ['']:

                    for number, img in enumerate(image_name, start=1):
                        if 'jpg' in img:
                            url_list.append(
                                {
                                    "ID": prod_id,
                                    "URL": f'https://moto-product-images.s3.us-east-2.amazonaws.com/{category}/{prod_id}/{prod_id}_{str(number)}.jpg',
                                }
                            )
                        elif 'png' in img:
                            url_list.append(
                                {
                                    "ID": prod_id,
                                    "URL": f'https://moto-product-images.s3.us-east-2.amazonaws.com/{category}/{prod_id}/{prod_id}_{str(number)}.png',
                                }
                            )
        f.close()

    # print(url_list)
    return url_list


# save_s3_urls()


# Loops thru s3 urls and creates master list for products with one and multiple images
def create_url_object():

    data = save_s3_urls()

    master_list = []

    img_list = []

    for i in data:

        current_record_id = i['ID']
        current_record_url = i['URL']

        if img_list == []:
            img_list.append({'id': current_record_id,
                            'url': current_record_url})
        elif img_list != []:
            if current_record_id == img_list[0]['id']:
                img_list.append({'id': current_record_id,
                                 'url': current_record_url})
            elif current_record_id != img_list[0]['id']:
                master_list.append(img_list)
                img_list = []
                img_list.append({'id': current_record_id,
                                 'url': current_record_url})

    master_object_list = []

    for obj in master_list:

        sub_object_list = []
        for img in obj:
            url = img['url']

            sub_object_list.append(url)

        master_object_list.append({"Id": obj[0]['id'], "Url": sub_object_list})

    # print(master_object_list)
    return master_object_list


# create_url_object()

#
# def write_urls_db():
#     data = create_url_object()
#
#     for i in data:
#         # print(i)
#         prod_code = i['Id']
#         s3_url = str(i['Url'])
#
#         s3_url = s3_url.replace('DigitalPro-TierMobileAccessories', 'Digital_Pro-Tier_Mobile_Accessories')
#         s3_url = s3_url.replace('PortableEarpieces', 'Portable_Earpieces')
#         s3_url = s3_url.replace('AnalogPro-TierMobileAccessories', 'Analog_Pro-Tier_Mobile_Accessories')
#         s3_url = s3_url.replace('LegacyVertexAccesories', 'Legacy_Vertex_Accesories')
#         s3_url = s3_url.replace('EarPieces', 'Ear_Pieces')
#         s3_url = s3_url.replace('CarryCases', 'Carry_Cases')
#         s3_url = s3_url.replace('PortableCarryAttachments', 'Portable_Carry_Attachments')
#         s3_url = s3_url.replace('PortableAntennas', 'Portable_Antennas')
#
#         s3_url = s3_url.replace('MobileServiceTools', 'Mobile_Service_Tools')
#         s3_url = s3_url.replace('PortableChargers', 'Portable_Chargers')
#         s3_url = s3_url.replace('Pro-TierDigitalAntennas', 'Pro-Tier_Digital_Antennas')
#         s3_url = s3_url.replace('PortableCables', 'Portable_Cables')
#         s3_url = s3_url.replace('ServiceToolsandMisc', 'Service_Tools_and_Misc')
#         s3_url = s3_url.replace('PortableServiceTools', 'Portable_Service_Tools')
#         s3_url = s3_url.replace('AnalogTrunkingMobileAccessories', 'Analog_Trunking_Mobile_Accessories')
#         s3_url = s3_url.replace('PortableRemoteSpeakerMicrophones', 'Portable_Remote_Speaker_Microphones')
#         s3_url = s3_url.replace('GeneralMobileAccessories', 'General_Mobile_Accessories')
#         s3_url = s3_url.replace('PortableBatteries', 'Portable_Batteries')
#         s3_url = s3_url.replace('MobileAntennas', 'Mobile_Antennas')
#         s3_url = s3_url.replace('MobileRadioAccessories', 'Mobile_Radio_Accessories')
#         s3_url = s3_url.replace('PortableHeadsets', 'Portable_Headsets')
#         s3_url = s3_url.replace('CallBoxes', 'Call_Boxes')
#
#         print(s3_url)
#
#         cursor.execute("UPDATE accessories SET imageUrls = ? WHERE sku = ?;", [str(s3_url), str(prod_code)])
#         conn.commit()
#
# # write_urls_db()
#
# def fix_table():
#     first = ['https://moto-radio-images.s3.us-east-2.amazonaws.com/Commercial/EVX-S24Portable/EVX-S24Portable_1.jpg', 'https://moto-radio-images.s3.us-east-2.amazonaws.com/Commercial/EVX-S24Portable/EVX-S24Portable_2.jpg']
#     second = ['https://moto-radio-images.s3.us-east-2.amazonaws.com/Commercial/CM200dMobile/CM200dMobile_1.png']
#
#     cursor.execute("UPDATE radios SET S3images = ? WHERE productName = 'EVX-S24 Portable';", [str(first)])
#     conn.commit()
#     cursor.execute("UPDATE radios SET S3images = ? WHERE productName = 'CM300d Mobile';", [str(second)])
#     conn.commit()
#
# # fix_table()
#
#
#
# def create_accessory():
#     cursor.execute("""CREATE TABLE accessories (
#                     id INTEGER PRIMARY KEY,
#                     sku BLOB,
#                     name BLOB,
#                     suggestedPrice REAL,
#                     description BLOB,
#                     info BLOB,
#                     compatible BLOB,
#                     categories BLOB,
#                     tags BLOB,
#                     imageUrls BLOB)""")
#     conn.commit()
#
# # create_accessory()
#
# def populate_accessory():
#     with open('accessories.csv', 'r', encoding='utf-8') as f:
#         r = csv.reader(f)
#         next(f)
#         id = 0
#         for row in r:
#             sku = row[0]
#             name = row[1]
#             price = row[2]
#             desc = row[3]
#             info = row[4]
#             compatible = row[5]
#             category = row[6]
#             tag = row[7]
#             imageUrl = row[8]
#             id+=1
#             cursor.executemany("INSERT INTO accessories values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
#                                [
#                                    (id, sku, name, price, desc, info, compatible, category, tag, imageUrl)
#                                ])
#             conn.commit()
#
# # populate_accessory()
#
# def drop_table():
#     cursor.execute("Drop table accessories")
#     conn.commit()
#
# # drop_table()
#
# def no_image():
#     url = 'http://cybercomm.flywheelsites.com/wp-content/uploads/2019/07/img_notavailable_insignia-01.png'
#     url2 = ['http://cybercomm.flywheelsites.com/wp-content/uploads/2019/07/img_notavailable_insignia-01.png']
#
#     cursor.execute("UPDATE accessories SET imageUrls = ? WHERE imageUrls = ?;", [str(url2), str(url)])
#     conn.commit()
#
# # no_image()
#
# def create_date():
#     date = '2019-7-11'
#     cursor.execute("UPDATE accessories SET created_date = ? WHERE sku = ?;", [str(date), str('0104036J89')])
#     conn.commit()
#     cursor.execute("UPDATE accessories SET last_updated_date = ? WHERE last_updated_date = ?;", [str(date), str(None)])
#     conn.commit()
#     cursor.execute("UPDATE accessories SET archived_date = ? WHERE archived_date = ?;", [str(date), str(None)])
#     conn.commit()
#
# # create_date()