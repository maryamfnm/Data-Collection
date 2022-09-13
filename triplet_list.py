import argparse
import json
import os
import random
import shutil

def parse_arguments():
    parser = argparse.ArgumentParser(description='arguments for creating triplet list')
    parser.add_argument('--start_id', type=int, default=530000)
    parser.add_argument('--end_id', type=int, default=530029)
    return parser.parse_args()

def clean():
    for json_id in range(args.start_id, args.end_id + 1):
        json_file = os.path.join(json_look_directory, '{}.json'.format(json_id))
        file_reader = json.load(open(json_file, 'r'))
        if len(file_reader) != 0:
            shutil.copy(json_file, "Json/clean_look/")

def create_triplet_list():
    tripletlist_train = os.path.join("tripletlists/", "tripletlist_train.txt")
    with open(tripletlist_train, 'a') as fp:
        for json_id in os.listdir(json_clean_look_directory):
            json_file = os.path.join(json_clean_look_directory, json_id)
            data = json.load(open(json_file, 'r'))
            products = data[0]["products"]
            random_products = random.sample(products, 2)
            tripletlist = []
            for product in random_products:
                item = random.sample(product, 1)
                tripletlist.append(item[0]["id"])

            files = os.listdir(json_clean_look_directory)
            filename = str(json_id) + '.json'
            third_look = random.sample([x for x in files if x != filename], 1)
            third_look_json = os.path.join(json_clean_look_directory, '{}'.format(third_look[0]))
            json_data = json.load(open(third_look_json, 'r'))
            _products = json_data[0]["products"]
            p = random.sample(_products, 1)
            third_product = random.sample(
                [i for i in p[0] if i['id'] != tripletlist[0] and i['id'] != tripletlist[1]], 1)
            tripletlist.append(third_product[0]["id"])
            for i in tripletlist:
                fp.write(i)
                fp.write(' ')
            fp.write('\n')

if __name__ == "__main__":
    json_look_directory = 'Json/Look/'
    json_clean_look_directory = 'Json/clean_look/'
    args = parse_arguments()
    if not os.path.isdir(json_clean_look_directory):
        os.mkdir(json_clean_look_directory)
    if not os.path.isdir("tripletlists/"):
        os.mkdir("tripletlists/")
    clean()
    create_triplet_list()

