import os

def images_per_product_count():
    directories = os.listdir(json_look_directory)
    for dir in directories:
        count = sum([len(files) for r, d, files in os.walk(json_look_directory + '/' + dir)])
        dictionary = {"product_id" : dir, "image_count" : count}
        images_per_product.append(dictionary)

if __name__ == "__main__":
    json_look_directory = '../Json/Product'
    images_per_product= []
    images_per_product_count()
