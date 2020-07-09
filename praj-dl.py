
# Web scraping program to download e-paper from the newspaper provider prajavani.

from selenium import webdriver
import requests
from datetime import date
import os
import PDFMerger

dateToday = date.today().strftime("%d-%m-%Y")

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


# Checking if the download button is enabled.
while True:
    downloadEnableCheck = driver.find_element_by_xpath('//*[@id="mainmenu"]/div/ul/li[7]').get_attribute('class')
    if downloadEnableCheck == 'printSaveFeature':
        click_download_button()
        break

# Load first page.
open_first_and_last_page()

# Loop to load all the middle pages.
for i in range(5):
    click_next_button()
    click_download_button()
    check_size_and_width_middle_pages()

# Sequence to load last page.
click_next_button()
click_download_button()
open_first_and_last_page()

folderPath = 'C:/Users/Sammy/Desktop/Prajavani ' + dateToday
os.makedirs(folderPath)  # Make a folder in desktop with today's date.

# Loop to download pages to the folder.
for i in range(12, 0, -1):
    driver.switch_to.window(driver.window_handles[i])
    res = requests.get(driver.current_url)
    res.raise_for_status()
    filePath = open(os.path.join(folderPath, str(i) + '.pdf'), 'wb')
    for chunk in res.iter_content(100000):
        filePath.write(chunk)
    filePath.close()

driver.quit()  # Close browser.

PDFMerger.merge_pdf_in_folder(folderPath, 'C:/Users/Sammy/Desktop')
