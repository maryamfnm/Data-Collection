import os

def total_count():
    total_image_count = 0
    directories = os.listdir(json_look_directory)
    for dir in directories:
        count = sum([len(files) for r, d, files in os.walk(json_look_directory + '/' + dir)])
        total_image_count = total_image_count + count
    return total_image_count
if __name__ == "__main__":
    json_look_directory = '../Json/Product'
    total_count = total_count()
    print("total_images_count" + str(total_count))