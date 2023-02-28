import os
import shutil
import requests
from bs4 import BeautifulSoup
from yaspin import yaspin
from progress.bar import ChargingBar
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options,

)
pins_list = []


def finding_images():
    global pins_list
    choise = input('If you want to use a ready link write 1, if you want to use keyword search write 2 (1/2): ')
    if choise == '1':
        url = input('Enter url: ')
    elif choise == '2':
        var = input('What kind of images do you need to download?: ')
        url = f"https://pinterest.com/search/pins/?q={var}"
    print('✅ Images search started')
    spinner = yaspin(text='Collecting urls')
    spinner.start()
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    for link in soup.find_all('a', href=True):
        if link.get('href').startswith('/pin/'):
            pin_url = f"https://www.pinterest.com{link.get('href')}"
            pins_list.append(pin_url)
        else:
            pass
    spinner.ok("✅")
    print(f'✅ Total media found: {len(pins_list)}')


def download_images():
    print('✅ Image download started')
    try:
        shutil.rmtree('images/')  # removing last images
    except Exception:
        pass
    os.makedirs(os.path.dirname('images/'), exist_ok=True)  # creating images folder
    counter = 0
    bar = ChargingBar('Downloading', max=len(pins_list))
    for url in pins_list:
        counter += 1
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        image = soup.find('img')
        image_link = image.get('src')
        filename = f'media_{counter}'
        img_data = requests.get(image_link).content
        with open(f'images/{filename}.jpg', 'wb') as handler:
            handler.write(img_data)
        bar.next()


def main():
    finding_images()
    download_images()
    driver.close()
    driver.quit()


main()
