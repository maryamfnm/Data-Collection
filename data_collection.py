import sys
import argparse
import json
import logging
import os
import re
import time
import requests
from random import randint
import urllib.request

from selenium import webdriver
from selenium.common.exceptions import (NoSuchElementException,
                                        StaleElementReferenceException)
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

logging.basicConfig(filename="log.log", level=logging.INFO)
chrome_options = Options()
chrome_options.add_argument("--incognito")
#chrome_options.add_argument("disable-infobars")
chrome_options.add_argument("disable-blink-features=AutomationControlled")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
#chrome_options.add_experimental_option('useAutomationExtension', False)


chrome_options.page_load_strategy = 'normal'
driver = webdriver.Chrome(chrome_options=chrome_options,
    executable_path="/Users/MaryamForootaninia/Downloads/chromedriver")
#driver = webdriver.Chrome(chrome_options=chrome_options,
                          #executable_path="/Users/Leader/Downloads/chromedriver")

look_url_template = ""
action = ActionChains(driver)


# Get the multiple options for each image if it exist
def images_options(_items):
    for item in _items:
        multiple_options = []
        product_ids = []
        try:
            driver.find_element_by_css_selector("a.acsCloseButton.acsAbandonButton").click()
        except NoSuchElementException:
            print("No Element Found")
        # Click on the item to load its other options in html
        time.sleep(5)
        item.click()

        # Getting the options for the items
        options = item.find_elements_by_tag_name("a._2_ZZl")
        for opt in options:
            image_src = opt.find_element_by_css_selector("img.Uz9Zj").get_attribute("src")
            image_src = re.sub(r'h=\d+', 'h=1196', image_src)
            image_src = re.sub(r'w=\d+', 'w=780', image_src)
            image_path = download_image(image_src, look_id, jpeg_look_directory, "")
            product_id = opt.get_attribute("href").split('/')[-1]
            image_data = {"id": product_id, "path": image_path}  # Get each product Id and path in a Look
            product_ids.append(image_data)
            multiple_options.append(opt.get_attribute("href"))  # Get the link for each option and add them to the list

        list_of_images.append(multiple_options)
        list_of_product_ids.append(product_ids)


# Download the image to JPEG directory
def download_image(image_src, product_id, directory, color_name):
    if directory == jpeg_product_directory:
        if color_name.__contains__("/"):
            color_name = color_name.replace("/", "_")
        if color_name.__contains__(" "):
            color_name = color_name.replace(" ", "_")
        _dir = directory + str(product_id) + '/' + color_name
    else:
        _dir = directory + str(product_id)

    image = image_src.split(".jpeg")
    image_id = image[0].split('/')[-1]

    if not os.path.isdir(_dir):
        os.makedirs(_dir)
    filename = os.path.join(_dir, image_id + '.jpeg')
    if os.path.isfile(filename):
        print("image file exist")
    else:
        urllib.request.urlretrieve(image_src, filename)
    return filename


def create_product_json(dictionary_object, product_id, color_name):
    if color_name.__contains__("/"):
        color_name = color_name.replace("/", "_")
    if color_name.__contains__(" "):
        color_name = color_name.replace(" ", "_")
    _dir = json_product_directory + str(product_id)
    if not os.path.isdir(_dir):
        os.makedirs(_dir)
    json_file = os.path.join(_dir, '{}.json').format(color_name)
    with open(json_file, 'w') as fp:
        json.dump(dictionary_object, fp)


def create_look_json(json_file):
    with open(json_file, 'w') as fp:
        if outfit_title != "":
            dictionary.insert(0, json_dictionary)
        json.dump(dictionary, fp)


def get_images_url(detailed_item_images, _look_id, _color_name_):
    images = []
    for detailed_image in detailed_item_images:
        # This if statement checks if the image is not a video
        if len(detailed_image.find_element_by_css_selector("img._3fwsO").get_attribute("srcset")) != 0:
            action.move_to_element(detailed_image)
            src_image = detailed_image.find_element_by_css_selector("img._3fwsO").get_attribute("src")

            # Get the src image which has a high resolution
            src_image = re.sub(r'h=\d+', 'h=1196', src_image)
            src_image = re.sub(r'w=\d+', 'w=780', src_image)

            if len(src_image) != 0:
                image_path = download_image(src_image, _look_id, jpeg_product_directory, _color_name_)
                image_data = {"url": src_image, "path": image_path}
                images.append(image_data)
    return images


# This is the main code which does the crawling work
def collect_data(_url_, sleep_time=3):
    counter = int(0)
    j = int(0)
    for img in list_of_images:
        k = int(0)
        for _image in img:
            _directory = json_product_directory + str(list_of_product_ids[j][k]["id"])

            # Checks if the product has already been scraped and directory has already been created
            if not os.path.isdir(_directory):
                driver.get(_image)
                time.sleep(sleep_time)
                if requests.get(_image).status_code != 200 or driver.current_url.__contains__("not-found"):
                    logging.info("Url does not exist " + _image + "\n")
                else:
                    image_title = driver.find_element_by_css_selector("h1._6YOLH._1JtW7._2VF_A._2OMMP").text
                    product_brand = driver.find_element_by_css_selector("span._1i-_6").text
                    try:
                        driver.find_element_by_css_selector("a.acsCloseButton.acsAbandonButton").click()
                    except (NoSuchElementException, StaleElementReferenceException) as e:
                        print("No pop up message exist \n")
                    full_list_of_images = []

                    try:
                        detailed_item_description = driver.find_elements_by_css_selector("._26GPU")
                        product_more_info = driver.find_elements_by_css_selector("._3RNkd")
                        product_detail = ""
                        product_size = ""
                        if len(product_more_info) == 2:
                            product_size_info = product_more_info[0].find_elements_by_css_selector("li.ErtZY")
                            for info in product_size_info:
                                product_size = product_size + '\n' + info.text

                            product_detail = product_more_info[1].find_element_by_css_selector("div._3LvFj p").text
                            details = product_more_info[1].find_elements_by_css_selector("li.ErtZY")
                            for text in details:
                                _text = text.text
                                product_detail = product_detail + '\n' + _text
                        else:
                            if product_more_info[0].find_elements_by_css_selector("li.ErtZY.div"):
                                for info in product_more_info[0].find_elements_by_css_selector("li.ErtZY"):
                                    product_size = product_size + '\n' + info.text
                            else:
                                if product_more_info[0].find_element_by_css_selector("div._3LvFj"):
                                    product_detail = product_more_info[0].find_element_by_css_selector(
                                        "div._3LvFj p").text
                                    details = product_more_info[0].find_elements_by_css_selector("li.ErtZY")
                                    for text in details:
                                        _text = text.text
                                        product_detail = product_detail + '\n' + _text

                    except NoSuchElementException:
                        detailed_item_description = ""
                        product_detail = ""
                        product_size = ""
                        print("Elements does does not exist for " + _image + "\n")

                    if detailed_item_description:
                        detailed_item_description = detailed_item_description[0].text
                    else:
                        detailed_item_description = ""

                    # if the item has multiple colors
                    if len(driver.find_elements_by_css_selector("button._3kLmr")) > 0:
                        # Find the list of the colors
                        colors = driver.find_elements_by_css_selector("button._3kLmr")
                        for _color in colors:
                            try:
                                driver.find_element_by_css_selector("a.acsCloseButton.acsAbandonButton").click()
                            except (NoSuchElementException, StaleElementReferenceException) as e:
                                print("No pop up message exist \n")
                            try:
                                # Click on each color button
                                action.move_to_element(_color)
                                time.sleep(5)
                                _color.click()
                            except StaleElementReferenceException:
                                print("StaleElementReferenceException" + _url_ + "\n")

                            # Get the list of images associated to that color
                            detailed_item_images = driver.find_elements_by_css_selector("li.BIgNz")

                            _color_name = _color.find_element_by_css_selector("img.zGPcv").get_attribute("alt")

                            # For each image in the list, click on it to get the higher resolution
                            detailed_images_list = get_images_url(detailed_item_images, list_of_product_ids[j][k]["id"],
                                                                  _color_name)
                            # Create a dictionary for each item
                            options = {
                                "product_id": list_of_product_ids[j][k]["id"],
                                "product_title": image_title,
                                "product_brand": product_brand,
                                "product_color": _color_name,
                                "product_description": detailed_item_description,
                                "product_details_and_care": product_detail,
                                "product_size_info": product_size,
                                "product_group": detailed_images_list
                            }

                            create_product_json(options, list_of_product_ids[j][k]["id"], _color_name)

                    # if the item doesn't have any color options
                    else:
                        # Get the list of images associated to that color
                        detailed_item_images = driver.find_elements_by_css_selector("li.BIgNz")
                        # loop through the image list for crawling data
                        for item_image in detailed_item_images:
                            # This if statement checks if the image is not a video
                            if len(item_image.find_element_by_css_selector("img._3fwsO").get_attribute("srcset")) != 0:
                                action.move_to_element(item_image)
                                _src_image_ = item_image.find_element_by_css_selector("img._3fwsO").get_attribute("src")

                                # Get the src image with high resolution
                                _src_image_ = re.sub(r'h=\d+', 'h=1196', _src_image_)
                                _src_image_ = re.sub(r'w=\d+', 'w=780', _src_image_)
                                if len(_src_image_) != 0:
                                    image_path = download_image(_src_image_, list_of_product_ids[j][k]["id"],
                                                                jpeg_product_directory, "")
                                    image_data = {"url": _src_image_, "path": image_path}
                                    full_list_of_images.append(image_data)

                        # Create the dictionary for the item
                        options = {
                            "product_id": list_of_product_ids[j][k]["id"],
                            "product_title": image_title,
                            "product_brand": product_brand,
                            "product_color": "",
                            "product_description": detailed_item_description,
                            "product_details_and_care": product_detail,
                            "product_size_info": product_size,
                            "product_group": full_list_of_images
                        }
                        _color_name = "no_color"
                        create_product_json(options, list_of_product_ids[j][k]["id"], _color_name)
                    counter = counter + 1
            else:
                print("Product Id " + list_of_product_ids[j][k]["id"] + " has already scraped")
            k = k + 1
        j = j + 1


def parse_arguments():
    parser = argparse.ArgumentParser(description='arguments for scraping looks meta data from nordstrom website')
    parser.add_argument('--look_url_template', default='https://www.nordstrom.com/look/{}')
    parser.add_argument('--start_id', type=int, default=530000)
    parser.add_argument('--end_id', type=int, default=530001)
    parser.add_argument('--sleep_after_look', default={'min': 1, 'max': 3}, help= \
        'number of seconds to sleep after each look. It will choose a random integer between in the specified range')
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()

    jpeg_look_directory = 'JPEG/Look/'
    jpeg_product_directory = 'JPEG/Product/'
    json_look_directory = 'Json/Look/'
    json_product_directory = 'Json/Product/'

    # Create JPEG/Look/
    if not os.path.isdir(jpeg_look_directory):
        os.makedirs(jpeg_look_directory)

    # Create JPEG/Product/
    if not os.path.isdir(jpeg_product_directory):
        os.makedirs(jpeg_product_directory)

    # Create Json/Look/
    if not os.path.isdir(json_look_directory):
        os.makedirs(json_look_directory)

    # Create Json/Product/
    if not os.path.isdir(json_product_directory):
        os.makedirs(json_product_directory)

    for look_id in range(args.start_id, args.end_id + 1):
        print('{}% , {} of [{},{}]'.format(100.0 * (look_id - args.start_id) / (args.end_id - args.start_id), look_id,
                                           args.start_id, args.end_id))
        output_file = os.path.join(json_look_directory, '{}.json').format(look_id)

        # initialize as empty
        urls = []
        items_ur = []
        dictionary = []
        elements = []
        list_of_images = []
        list_of_product_ids = []

        if not os.path.exists(output_file):
            look_url = args.look_url_template.format(look_id)
            driver.get(look_url)
            time.sleep(10)

            # This is returning the category of the set. i.e HANGING OUT or A CASUAL SPRING DAY
            try:
                outfit_title = driver.find_element_by_class_name(".EpVZP").text
            except NoSuchElementException:
                outfit_title = ""
            if outfit_title != "":
                try:
                    # Get the items of the collection
                    items = driver.find_elements_by_css_selector("div._17MDx")

                    # Find the options of each item if they exist
                    images_options(items)

                    json_dictionary = {
                        "look_id": look_id,
                        "look_title": outfit_title,
                        "products": list_of_product_ids
                    }

                    # Crawl data
                    collect_data(look_url)

                except NoSuchElementException:
                    logging.info("Invalid url " + look_url + "\n")

            # write data to json file
            create_look_json(output_file)

            logging.info("saved look id {}".format(look_id))

            # Add random sleep time
            time.sleep(randint(args.sleep_after_look['min'], args.sleep_after_look['max']))
        else:
            logging.info("look id {} already exists: {}".format(look_id, output_file))
sys.exit(0)
