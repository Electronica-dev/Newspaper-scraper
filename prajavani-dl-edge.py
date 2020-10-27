
# Web scraping program to download e-paper from the newspaper provider Prajavani, and send it to an email. Edge
# compatible version.

from selenium import webdriver
import requests
from datetime import date
from datetime import timedelta
from os import makedirs
from os import path
from os import remove
from os import environ
from shutil import rmtree
from PDFMerger import merge_pdf_in_folder
from send_email import send_email_pdf
from sys import exit
from sys import argv
from math import ceil
from time import sleep
import traceback

if len(argv) < 4:
    print('''Usage: prajavani-dl-edge.py [directory-location] [file-size] [recipient-email-address 1] [recipient-email-address 2] [
          recipient-email-address n]''')
    exit()
else:
    pathToDirectory = str(argv[1])
    size = int(argv[2])
    recipientAddress = argv[3:]
    if str.lower(pathToDirectory) == 'desktop':
        pathToDirectory = path.join(environ['USERPROFILE'], 'Desktop')
        print(pathToDirectory)
    elif not path.isdir(pathToDirectory):
        print('The provided directory doesn\'t exist')
        exit()

dateToday = date.today().strftime("%d-%m-%Y")
dateYesterday = (date.today() - timedelta(days = 1)).strftime("%d-%m-%Y")

yesterdayFileOne = pathToDirectory + '/Prajavani part 1 ' + dateYesterday + '.pdf'
yesterdayFileTwo = pathToDirectory + '/Prajavani part 2 ' + dateYesterday + '.pdf'

if path.isfile(yesterdayFileOne):
    remove(yesterdayFileOne)
if path.isfile(yesterdayFileTwo):
    remove(yesterdayFileTwo)

try:
    driver = webdriver.Edge(executable_path='path/to/webdriver')

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

    # First and last page are shown up individually.
    def open_first_and_last_page():
        while True:
            thumbnail_container_width = int(driver.find_element_by_xpath('//*[@id="leftPageThumb"]/div/div[3]').size.get(
                'width'))
            if thumbnail_container_width > 77:
                click_open_left_page()
                driver.switch_to.window(driver.window_handles[0])
                click_close_button()
                break

    # Checking if the size is shown and page thumbnail is loaded.
    def check_size_and_width_middle_pages():
        while True:
            left_thumbnail_container_width = int(driver.find_element_by_xpath('//*[@id="leftPageThumb"]/div/div[3]').size.get('width'))
            right_thumbnail_container_width = int(driver.find_element_by_xpath('//*[@id="rightPageThumb"]/div/div[3]').size.get('width'))
            if left_thumbnail_container_width > 77 and right_thumbnail_container_width > 77:
                click_open_left_page()
                driver.switch_to.window(driver.window_handles[0])
                click_open_right_page()
                driver.switch_to.window(driver.window_handles[0])
                click_close_button()
                break


    # Checking if the menu toolbar has loaded.
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
    page_no = 1
    folderNo = 1

    folderPath = pathToDirectory + '/Prajavani part ' + str(folderNo) + ' ' + dateToday #  Initial folder path with today's date.
    makedirs(folderPath)  # Make that folder.

    while(page_no <= noOfPages):

        if (size != 0 and total_file_size > (size * 1000000)):
            total_file_size = 0
            folderNo += 1
            folderPath = pathToDirectory + '/Prajavani part ' + str(folderNo) + ' ' + dateToday
            makedirs(folderPath)

        print('Downloading page ' + str(page_no))
        driver.switch_to.window(driver.window_handles[page_no])
        res = requests.get(driver.current_url)
        res.raise_for_status()
        file_size = int(res.headers.get('Content-Length', None))
        total_file_size += file_size
        filePath = open(path.join(folderPath, str(page_no) + '.pdf'), 'wb')
        for chunk in res.iter_content(100000):
            filePath.write(chunk)
        filePath.close()
        page_no += 1

    driver.quit()  # Close browser.

    for i in range(folderNo):
        merge_pdf_in_folder((pathToDirectory + '/Prajavani part ' + str(i + 1) + ' ' + dateToday), pathToDirectory, 'Prajavani part ' + str(i + 1) + ' ' + dateToday)
        rmtree(pathToDirectory + '/Prajavani part ' + str(i + 1) + ' ' + dateToday)
        send_email_pdf(recipientAddress, [pathToDirectory + '/Prajavani part '+ str(i + 1) + dateToday + '.pdf'],
                    subject='Prajavani Newspaper part ' + str(i + 1) + dateToday)

except:

    error_file = open('error_info.txt', 'w')
    error_file.write(traceback.format_exc())
    error_file.close()
