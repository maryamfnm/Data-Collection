import glob
import json
import os
from pathlib import Path
import itertools
from imutils import build_montages
import cv2


'''def Montage(image_paths,look_id, indx):
    collage = []
    for image_path in image_paths:
        # load the image and update the list of images
        image = cv2.imread(image_path['image'])
        collage.append(image)
    # construct the montages for the images
    montages = build_montages(collage, (780, 1196), (125, 78))
    _dir = os.path.join(collage_Look_directory, look_id)
    if not os.path.isdir(_dir):
        os.makedirs(_dir)
    filename = os.path.join(_dir, str(indx) + '.jpeg')
    if not os.path.isfile(filename):
        collage_file = os.path.join(filename)
        cv2.imwrite(collage_file, montages)'''


def convert():
    list_of_dictionaries = []
    for look in glob.glob(json_look_file + "/*.json"):
        _file = open(look, "r")
        data = json.load(_file)
        if len(data) != 0:
            iterlist = data[0]['products']
            _combinations = list(itertools.product(*iterlist))

            for product in _combinations:
                items = []
                i = 0
                for option in product:
                    i += 1
                    categoryid = option['id']
                    image = option['path']
                    product_path = json_product_file + '/' + categoryid + '.json'
                    path = Path(product_path)
                    if path.is_file():
                        fr = open(product_path, 'r')
                        product_json = json.load(fr)
                        name = product_json['product_title']
                        item = {
                            "index": i,
                            "name": name,
                            "price": -1,
                            "likes": -1,
                            "image": image,
                            "categoryid": categoryid
                        }
                        items.append(item)
                #Montage(items, str(data[0]['look_id']), i)
                look_dictionary = {
                    "name": data[0]['look_title'],
                    "views": -1,
                    "items": items,
                    "image": "",
                    "likes": -1,
                    "date": "",
                    "set_url": "https://shop.nordstrom.com/look/" + str(data[0]['look_id']),
                    "set_id": data[0]['look_id'],
                    "desc": ""
                }
                list_of_dictionaries.append(look_dictionary)
    with open("train.json", 'a') as fp:
        json.dump(list_of_dictionaries, fp)


if __name__ == "__main__":
    json_look_file = "Json/Look"
    json_product_file = "Json/Product"
    collage_Look_directory = "Collage/Look/"
    new_dic = []
    if not os.path.isfile("train.json"):
        train_json = os.path.join("train.json")
    # Create Collage/Look/
    if not os.path.isdir(collage_Look_directory):
        os.makedirs(collage_Look_directory)
    convert()
