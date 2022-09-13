import glob
import json

def products_per_look():
    for f in glob.glob(json_look_directory + '/*.json', recursive=True):
        json_file = open(f,'r')
        data = json.load(json_file)
        if (len(data) != 0):
            products_per_look_list = []
            count = 0
            for product_list in data[0]["products"]:
                for product in product_list:
                    if not(products_per_look_list.__contains__(product["id"])):
                        products_per_look_list.append(product["id"])
                        count += 1
            dictionary = {"look_id": data[0]["look_id"], "products_per_look_count": count,
                          "products_per_look_list": products_per_look_list }
            images_per_product.append(dictionary)

if __name__ == "__main__":
    json_look_directory = '../Json/Look'
    images_per_product= []
    products_per_look()
    print("done")