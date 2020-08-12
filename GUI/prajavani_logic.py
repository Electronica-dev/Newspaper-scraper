
""" Scrape e-paper from the newspaper provider Prajavani, and send it to an email. Edge version. """

from datetime import date
from os import makedirs
from os import path
from shutil import rmtree
import traceback
from math import ceil
from time import sleep
from selenium import webdriver
import requests
from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal
from PDFMerger import merge_pdf_in_folder
from send_email import send_email_pdf


class DownloadPrajavani(QThread):

    dateToday = date.today().strftime("%d-%m-%Y")

    percentage_signal_pr = pyqtSignal(int)
    page_no_signal_pr = pyqtSignal(str)
    done_signal_pr = pyqtSignal(bool)
    start_signal_pr = pyqtSignal(bool)
    error_signal_pr = pyqtSignal(str)
    pdf_progress_signal_pr = pyqtSignal(str)
    email_progress_signal_pr = pyqtSignal(str)

    def __init__(self, directory_path, recipient_address_list):
        super().__init__()
        self.directory_path = directory_path
        self.recipient_address_list = [ele.strip() for ele in recipient_address_list.split(',')]

    def run(self):

        try:
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
                download_enable_check = driver.find_element_by_xpath('//*[@id="mainmenu"]/div/ul/li[7]').get_attribute('class')
                if download_enable_check == 'printSaveFeature':
                    sleep(8)
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

            path_ = self.directory_path + '//Prajavani ' + self.dateToday
            makedirs(path_)  # Make a folder in desktop with today's date.

            self.start_signal_pr.emit(True)  # signal to let the main gui know that all pages have been loaded

            # Loop to download pages to the folder.
            # for i in range(1, 2):
            for i in range(1, (no_of_pages + 1)):
                self.page_no_signal_pr.emit(str(i))
                driver.switch_to.window(driver.window_handles[i])
                page_pdf = requests.get(driver.current_url, stream=True)
                page_pdf.raise_for_status()
                file_size = int(page_pdf.headers.get('Content-Length', None))
                progress = 0
                with open(path.join(path_, str(i)), 'wb') as f:
                    for data in page_pdf:
                        f.write(data)
                        progress += len(data)
                        percentage = (progress/file_size)*100
                        self.percentage_signal_pr.emit(int(percentage))
                    f.close()
                    sleep(0.2)
                    self.percentage_signal_pr.emit(0)

            self.done_signal_pr.emit(True)  # signal to let the main gui know that the process has completed.

            driver.quit()  # Close browser.

            self.pdf_progress_signal_pr.emit('Creating combined pdf')
            merge_pdf_in_folder(path_, self.directory_path, 'Prajavani ' + self.dateToday)
            self.pdf_progress_signal_pr.emit('Combined pdf created')

            rmtree(path_)

            if self.recipient_address_list != ['']:

                self.email_progress_signal_pr.emit('Sending email')
                send_email_pdf(self.recipient_address_list, [self.directory_path + r'/Prajavani '+self.dateToday +
                                                             '.pdf'],
                               subject='Prajavani Newspaper ' + self.dateToday)
                self.email_progress_signal_pr.emit('Email sent successfully')

        except FileExistsError as file_error:
            
            self.error_signal_pr.emit(str(file_error))

        except:

            self.error_signal_pr.emit('Error occured. Written to error_info_pr.txt.')
            error_file = open('error_info_pr.txt', 'w')
            error_file.write(traceback.format_exc())
            error_file.close()
