import os
import argparse


def getListOfFiles(_directory):
    list_of_files = os.listdir(_directory)
    all_files = []
    for entry in list_of_files:
        full_path = os.path.join(_directory, entry)
        if os.path.isdir(full_path):
            all_files = all_files + getListOfFiles(full_path)
        else:
            all_files.append(full_path)
    return all_files


def run_visualization(directory):
    images = getListOfFiles(directory)
    with open(html_file, 'a') as fp:
        fp.write("<table style='border:1px solid black'>"
                 "<tr>"
                 "<th>Product Id</th>"
                 "<th align='left'>Product Images</th>"
                 "</tr>")
        for sub_dir in os.listdir(directory):
            fp.write("<tr>")
            if not sub_dir.startswith('.'):
                product_id = "<tr><td>{}</td>".format(sub_dir)
                fp.write(product_id)
                for image in images:
                    if not image.__contains__(".DS_Store"):
                        row = "<td><img src='{}' width=95 height=65></img></td>".format("../" + image)
                        fp.write(row)
                fp.write("</tr></table>")
            fp.write("</tr>")


def parse_arguments():
    parser = argparse.ArgumentParser(description='arguments for visualizing clean data')
    parser.add_argument('--path', type=str, default="/Users/MaryamForootaninia/JPEG/Product")
    return parser.parse_args()


if __name__ == "__main__":
    clean_data = 'HTML/Clean/'
    args = parse_arguments()
    if not os.path.isdir(clean_data):
        os.makedirs(clean_data)

    filepath = clean_data + 'clean_data.html'
    if not os.path.isfile(filepath):
        html_file = os.path.join(filepath)

    run_visualization(args.path)
