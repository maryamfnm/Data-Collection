from selenium import webdriver

from selenium.webdriver.chrome.options import Options



chrome_options = Options()

chrome_options.add_argument("--incognito")

chrome_options.add_argument("--window-size=1920x1080")



driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="/Users/Leader/Downloads/chromedriver")



import time

url = "https://shop.nordstrom.com/s/nike-icon-clash-dri-fit-tank/5449638?origin=category-personalizedsort&breadcrumb=Home%2FWomen%2FClothing%2FActivewear&color=black"

driver.get(url)

time.sleep(2)



elements = driver.find_elements_by_css_selector(".BIgNz")

print(elements)





images= driver.find_elements_by_tag_name("img")

print(images)

for image in images:

    src = image.get_attribute("src")

    print(src)
