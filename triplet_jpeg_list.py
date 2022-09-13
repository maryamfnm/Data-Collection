import os
import random

def create_triplet_list():
    tripletlist_train = os.path.join("tripletlists/", "tripletlist_jpeg.txt")
    folders = os.listdir(jpeg_look_directory)
    with open(tripletlist_train, 'a') as fp:
        for id in os.listdir(jpeg_look_directory):
            if not id.startswith('.'):
                files = os.listdir(jpeg_look_directory + str(id))
                products = random.sample(files, 2)
                products[0] = os.path.join(jpeg_look_directory,id, products[0])
                products[1] = os.path.join(jpeg_look_directory, id, products[1])
                third_product_directory = random.sample([dir for dir in folders if dir != str(id)], 1)
                _files = [f for f in os.listdir(jpeg_look_directory + third_product_directory[0]) if f != ".DS_Store"]
                third_product = random.sample([i for i in _files if i != products[0] and i != products[1]], 1)
                third_product[0] = os.path.join(jpeg_look_directory,str(third_product_directory[0]), third_product[0])
                triplet = [products[0],products[1],third_product[0]]
                for i in triplet:
                    fp.write(i)
                    fp.write(' ')
                fp.write('\n')

if __name__ == "__main__":
    jpeg_look_directory = 'JPEG/Look/'
    #filtered_jpeg_look = 'Json/filtered_jpeg_look/'
    if not os.path.isdir(jpeg_look_directory):
        os.mkdir(jpeg_look_directory)
    if not os.path.isdir("tripletlists/"):
        os.mkdir("tripletlists/")
    create_triplet_list()