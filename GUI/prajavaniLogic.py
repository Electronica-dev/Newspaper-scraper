
"""Web scraping program to download e-paper from the newspaper provider Prajavani, and send it to an email. Edge
compatible version."""

from selenium import webdriver
import requests
from datetime import date
from os import makedirs
from shutil import rmtree
from PDFMerger import merge_pdf_in_folder
from send_email import send_email_pdf
from math import ceil
from time import sleep

dateToday = date.today().strftime("%d-%m-%Y")


def prajavani_download(directory_path, recipient_address_list):
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

    # First and last page are shown up individually.
    def open_first_and_last_page():
        while True:
            thumbnail_container_width = driver.find_element_by_xpath('//*[@id="leftPageThumb"]/div/div[3]').size.get(
                'width')
            if thumbnail_container_width == 141:
                click_open_left_page()
                driver.switch_to.window(driver.window_handles[0])
                click_close_button()
                break

    # Checking if the size is shown and page thumbnail is loaded.
    def check_size_and_width_middle_pages():
        while True:
            left_thumbnail_container_width = driver.find_element_by_xpath('//*[@id="leftPageThumb"]/div/div[3]').size.get(
                'width')
            right_thumbnail_container_width = driver.find_element_by_xpath('//*[@id="rightPageThumb"]/div/div[3]').size.get(
                'width')
            if left_thumbnail_container_width == 141 and right_thumbnail_container_width == 141:
                click_open_left_page()
                driver.switch_to.window(driver.window_handles[0])
                click_open_right_page()
                driver.switch_to.window(driver.window_handles[0])
                click_close_button()
                break

    # Checking if the menu toolbar has loaded.
    while True:
        menu_width_check = int(driver.find_element_by_xpath('//*[@id="mainmenu"]/div').size.get('width'))
        if menu_width_check == 438:
            driver.find_element_by_id('btnPublicationsPanel').click()
            driver.find_element_by_id('pubFilterEdition').click()
            driver.find_element_by_xpath('//*[@id="pubFilterEdition"]/option[3]').click()
            break

    while True:
        sleep(2)
        download_enable_check = driver.find_element_by_xpath('//*[@id="mainmenu"]/div/ul/li[7]').get_attribute('class')
        if download_enable_check == 'printSaveFeature':
            click_download_button()
            no_of_pages = int(driver.find_element_by_xpath('//*[@id="tpContainer"]/h3/small').get_attribute(
                'data-pginsection'))
            break

    # Load first page.
    open_first_and_last_page()

    # Loop to load all the middle pages.
    for i in range(int(ceil(no_of_pages - 2) / 2)):
        click_next_button()
        click_download_button()
        check_size_and_width_middle_pages()

    # Sequence to load last page.
    if not no_of_pages % 2:
        click_next_button()
        click_download_button()
        open_first_and_last_page()

    path_ = directory_path + dateToday
    makedirs(path_)  # Make a folder in desktop with today's date.

    # Loop to download pages to the folder.
    for i in range(1, (no_of_pages + 1)):
        print('Downloading page ' + str(i))
        driver.switch_to.window(driver.window_handles[i])
        res = requests.get(driver.current_url)
        res.raise_for_status()
        file_path = open(path_.join(path_, str(i) + '.pdf'), 'wb')
        for chunk in res.iter_content(100000):
            file_path.write(chunk)
        file_path.close()

    driver.quit()  # Close browser.

    merge_pdf_in_folder(path_, 'C:/Users/Sammy/Desktop', 'Prajavani ' + dateToday)

    rmtree(path_)

    if recipient_address_list != ['']:
        send_email_pdf(recipient_address_list, [r'C:/Users/Sammy/Desktop/Prajavani '+dateToday + '.pdf'],
                       subject='Prajavani Newspaper ' + dateToday)
