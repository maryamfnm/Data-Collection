import glob
import json
import os
import argparse


# Get the products images for a look
def get_products(_id):
    img_tag = "<td border-style: 4px solid black>"
    _directory = jpeg_product_directory + str(_id)
    for subdir, dirs, files in os.walk(_directory):
        if len(dirs) != 0:
            for _dir in dirs:

                for product_img in glob.glob(subdir + '/' + _dir + '/*.jpeg', recursive=True):
                    img_tag += "<img src='{}' width=95 height=65></img>".format('../../' + product_img)
        else:
            for f in files:
                for product_img in glob.glob(subdir + '/' + f + '/*.jpeg', recursive=True):
                    img_tag += "<img src='{}' width=95 height=65></img>".format('../../' + product_img)
    img_tag += "</td>"
    return img_tag


# Create html for each look and the corresponding products
def look_product_visualization(_args):
    if not os.path.isdir(html_look_directory):
        os.makedirs(html_look_directory)
    for json_id in range(_args.start_id, _args.end_id + 1):
        json_file = os.path.join(json_look_directory, '{}.json'.format(json_id))
        data = json.load(open(json_file, 'r'))
        html_file = os.path.join(html_look_directory, '{}.html').format(data[0]["look_id"])
        products = data[0]["products"]
        with open(html_file, 'w') as fp:
            fp.write("<table style='border:1px solid black'>"
                     "<tr>"
                     "<th border-style: 4px solid black>Look Id</th>"
                     "<th border-style: 4px solid black>Product Id</th>"
                     "<th border-style: 4px solid black>Look Image</th>"
                     "<th border-style: 4px solid black>Product Images</th>"
                     "</tr>")
            for product in products:
                for item in product:
                    product_id = item['id']
                    look_img = item['path']
                    img_tag = get_products(product_id)
                    _html = "<tr style='border:4px solid black margin:1px'><td border: 4px solid black>{}</td><td " \
                            "border: " \
                            "4px solid black>{}</td><td border: 4px solid black><img src='{}' width=95 " \
                            "height=65></img></td>{}</tr>" \
                        .format(data[0]["look_id"], product_id, '../../' + look_img, img_tag)
                    fp.write(_html)


def parse_arguments():
    parser = argparse.ArgumentParser(description='arguments for visualizing look and product images')
    parser.add_argument('--start_id', type=int, default=530000)
    parser.add_argument('--end_id', type=int, default=530010)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    json_look_directory = 'Json/Look/'
    html_look_directory = 'HTML/Look/'
    jpeg_product_directory = 'JPEG/Product/'


    look_product_visualization(args)
