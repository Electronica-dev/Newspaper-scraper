
# Web scraping program to download e-paper from the newspaper provider Prajavani, and send it to an email. Chrome
# and Edge compatible version.

from selenium import webdriver
import requests
import re
from argparse import ArgumentParser
from argparse import ArgumentTypeError
from datetime import date
from datetime import timedelta
from os import makedirs
from os import path
from os import remove
from os import environ
from shutil import rmtree
from pathlib import Path
from sys import exit
from sys import argv
from math import ceil
from time import sleep
import traceback
from PDFMerger import merge_pdf_in_folder
from send_email import send_email_pdf

parser = ArgumentParser()
parser.add_argument("browser", help="choose your preferred browser (c for Chrome and e for Edge)", choices=['c', 'e', 'C', 'E'])
parser.add_argument("--directory", "-d", help = "choose directory location (desktop, documents, downloads or your own)", default='desktop', type=str.lower)
def check_positive(value):
    val = int(value)
    if val < 0:
        raise ArgumentTypeError("Invalid size")
    return val
parser.add_argument("--size", "-s", help="specify file size", type=check_positive, default=0)
parser.add_argument("--mail", "-m", help="send mail", nargs='+')
parser.add_argument("--delete", "-del", help="delete previous day's files", action='store_true')
args = parser.parse_args()

browser = args.browser
pathToDirectory = args.directory
size = args.size
recipientAddress = args.mail

if pathToDirectory == 'desktop':
    pathToDirectory = path.join(environ['USERPROFILE'], 'Desktop')
elif pathToDirectory == 'documents':
    pathToDirectory = path.join(environ['USERPROFILE'], 'Documents')
elif pathToDirectory == 'downloads':
    pathToDirectory = path.join(environ['USERPROFILE'], 'Downloads')
elif not path.isdir(pathToDirectory):
    print('Folder/path does not exist')

if args.delete:
    dateYesterday = (date.today() - timedelta(days = 1)).strftime("%d-%m-%Y")
    yesterdayFilePath = Path(pathToDirectory)
    yesterdayFileList = list(yesterdayFilePath.glob('Prajavani part ? ' + dateYesterday + '.pdf'))

    for file in yesterdayFileList:
        if(path.isfile(file)):
            remove(file)

dateToday = date.today().strftime("%d-%m-%Y")

try:
    if (browser.lower() == 'c'):
        driver = webdriver.Chrome()
    elif (browser.lower() == 'e'):
        driver = webdriver.Edge()

    driver.get('http://epaper.prajavani.net')  # Base url.
    driver.maximize_window()  # Maximizing window, else the downloadButton element won't be click-able.


    def click_download_button():
        download_button = driver.find_element_by_xpath('//*[@id="btnPrintSave"]')
        download_button.click()


    def click_close_button():
        close_button = driver.find_element_by_xpath('//*[@id="printSavePanel"]/div/div/div[1]/div/div/ul/li')
        close_button.click()


    def click_next_button():
        next_button = driver.find_element_by_id('btn-next')
        next_button.click()


    def click_open_left_page():
        left_page = driver.find_element_by_xpath('//*[@id="leftPageThumb"]/div/div[3]')
        left_page.click()


    def click_open_right_page():
        right_page = driver.find_element_by_xpath('//*[@id="rightPageThumb"]/div/div[3]')
        right_page.click()

    pattern = re.compile(r'epaper.prajavani.net')
    def check_ad():
        while True:
            driver.switch_to.window(driver.window_handles[1])
            website = pattern.findall(driver.current_url)
            if website:
                return True
            else:
                driver.close()

    # First and last page are shown up individually.
    def open_first_and_last_page():
        while True:
            thumbnail_container_width = driver.find_element_by_xpath('//*[@id="leftPageThumb"]/div/div[3]').size.get(
                'width')
            if thumbnail_container_width > 77:
                click_open_left_page()
                driver.switch_to.window(driver.window_handles[0])
                click_close_button()
                break


    # Checking if the size is shown and page thumbnail is loaded.
    def check_size_and_width_middle_pages():
        while True:
            left_thumbnail_container_width = driver.find_element_by_xpath('//*[@id="leftPageThumb"]/div/div[3]').size.get('width')
            right_thumbnail_container_width = driver.find_element_by_xpath('//*[@id="rightPageThumb"]/div/div[3]').size.get('width')
            if left_thumbnail_container_width > 77 and right_thumbnail_container_width > 77:
                click_open_left_page()
                driver.switch_to.window(driver.window_handles[0])
                click_open_right_page()
                driver.switch_to.window(driver.window_handles[0])
                click_close_button()
                break


    # Checking if the menu toolbar has loaded and selecting Uttara Kannada version of newspaper.
    while True:
        menuWidthCheck = int(driver.find_element_by_xpath('//*[@id="mainmenu"]/div').size.get('width'))
        if menuWidthCheck == 438:
            driver.find_element_by_id('btnPublicationsPanel').click()
            driver.find_element_by_id('pubFilterEdition').click()
            driver.find_element_by_xpath('//*[@id="pubFilterEdition"]/option[3]').click()
            break

    while True:
        downloadEnableCheck = driver.find_element_by_xpath('//*[@id="mainmenu"]/div/ul/li[7]').get_attribute('class')
        loadingBar = int(driver.find_element_by_xpath('//*[@id="loadingProgress"]').get_attribute('value'))
        if downloadEnableCheck == 'printSaveFeature' and loadingBar == 9 and menuWidthCheck == 438:
            sleep(10)
            click_download_button()
            noOfPages = int(driver.find_element_by_xpath('//*[@id="tpContainer"]/h3/small').get_attribute(
                'data-pginsection'))
            break

    # Load first page.
    open_first_and_last_page()

    # Loop to load all the middle pages.
    for i in range(int(ceil(noOfPages - 2) / 2)):
        click_next_button()
        click_download_button()
        check_size_and_width_middle_pages()

    # Sequence to load last page.
    if not noOfPages % 2:
        click_next_button()
        click_download_button()
        open_first_and_last_page()

    total_file_size = 0
    pages_downloaded = 0
    folderNo = 1

    folderPath = pathToDirectory + '/Prajavani part ' + str(folderNo) + ' ' + dateToday #  Initial folder path with today's date.
    makedirs(folderPath)  # Make that folder.

    while (len(driver.window_handles) > 1):

        if (size != 0 and total_file_size > (size * 1000000)):
            total_file_size = 0
            folderNo += 1
            folderPath = pathToDirectory + '/Prajavani part ' + str(folderNo) + ' ' + dateToday
            makedirs(folderPath)

        if check_ad():
            driver.switch_to.window(driver.window_handles[1])
            print('Downloading page ' + str(pages_downloaded + 1))
            res = requests.get(driver.current_url)
            res.raise_for_status()
            file_size = int(res.headers.get('Content-Length', None))
            total_file_size += file_size
            filePath = open(path.join(folderPath, str(pages_downloaded + 1) + '.pdf'), 'wb')
            for chunk in res.iter_content(100000):
                filePath.write(chunk)
            filePath.close()
            driver.close()
            pages_downloaded += 1

    driver.quit()  # Close browser.

    for i in range(folderNo):
        merge_pdf_in_folder((pathToDirectory + '/Prajavani part ' + str(i + 1) + ' ' + dateToday), pathToDirectory, 'Prajavani part ' + str(i + 1) + ' ' + dateToday)
        rmtree(pathToDirectory + '/Prajavani part ' + str(i + 1) + ' ' + dateToday)
        if recipientAddress:
            send_email_pdf(recipientAddress, [pathToDirectory + '/Prajavani part '+ str(i + 1) + dateToday + '.pdf'],
                    subject='Prajavani Newspaper part ' + str(i + 1) + dateToday)

except:

    error_file = open('error_info.txt', 'w')
    error_file.write(traceback.format_exc())
    error_file.close()