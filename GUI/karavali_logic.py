""" Scrape e-paper from the newspaper provider Karavali Munjavu, and send it to an email. Edge version. """

from datetime import date
from os import makedirs
from os import path
from os import listdir
from shutil import rmtree
from time import sleep
import traceback
from requests import get
from PIL import Image
from bs4 import BeautifulSoup
from img2pdf import convert
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QThread
from PDFMerger import merge_pdf_in_folder
from send_email import send_email_pdf


class DownloadKaravali(QThread):

    percentage_signal_kr = pyqtSignal(int)
    page_no_signal_kr = pyqtSignal(str)
    done_signal_kr = pyqtSignal(bool)
    start_signal_kr = pyqtSignal(bool)
    error_signal_kr = pyqtSignal(str)
    pdf_progress_signal_kr = pyqtSignal(str)
    email_progress_signal_kr = pyqtSignal(str)

    date_today = date.today().strftime("%d-%m-%Y")

    def __init__(self, directory_path, recipient_address_list):

        super().__init__()
        self.directory_path = directory_path
        self.recipient_address_list = [ele.strip() for ele in recipient_address_list.split(',')]

    def run(self):

        try:
            folder_path_img = self.directory_path + r'/Karavali Munjavu ' + self.date_today
            folder_path_pdf = self.directory_path + r'/Karavali Munjavu pdf ' + self.date_today
            makedirs(folder_path_img)  # Make a folder in desktop with today's date.

            url = 'http://www.karavalimunjavu.com/'
            res = get(url)
            res.raise_for_status()
            soup = BeautifulSoup(res.text, 'lxml')

            self.start_signal_kr.emit(True)

            # Downloading images.
            for images in soup.select('img[data-big]'):
                page_no = str(path.basename(images.get('data-big'))[15:])
                self.page_no_signal_kr.emit(page_no)
                img_download = get(url+images.get('data-big'), stream=True)
                file_size = int(img_download.headers.get("Content-Length", None))
                progress = 0
                with open(path.join(folder_path_img, page_no), 'wb') as f:
                    for data in img_download:
                        f.write(data)
                        progress += len(data)
                        percentage = (progress/file_size)*100
                        self.percentage_signal_kr.emit(round(percentage, 0))
                    f.close()
                    sleep(0.2)
                    self.percentage_signal_kr.emit(0)
            
            makedirs(folder_path_pdf)

            # Converting images to pdf.
            print('Converting images to pdf')
            for page in listdir(folder_path_img):
                pdf_bytes = convert(Image.open(folder_path_img+'//'+page).filename)
                file = open(path.join(folder_path_pdf, page[:-4] + '.pdf'), 'wb')
                file.write(pdf_bytes)
                file.close()
            print('Images converted to pdf.')

            rmtree(folder_path_img)  # Deleting folder containing images.

            self.pdf_progress_signal_kr.emit('Creating combined PDF')
            merge_pdf_in_folder(folder_path_pdf, self.directory_path, 'Karavali Munjavu ' + str(self.date_today)) # Merging PDFs
            self.pdf_progress_signal_kr.emit('Combined PDF created')

            rmtree(folder_path_pdf)  # Deleting folder containing pdfs.

            self.done_signal_kr.emit(True)  # signal to let the main gui know that the process has completed.

            if self.recipient_address_list != ['']:
                
                self.email_progress_signal_kr.emit('Sending email')
                send_email_pdf(self.recipient_address_list, [self.directory_path + r'/Karavali Munjavu '+self.date_today +
                                                             '.pdf'],
                               subject='Karavali Munjavu Newspaper ' + self.date_today)
                self.email_progress_signal_kr.emit('Mail sent successfully')

        except FileExistsError as file_error:

            self.error_signal_kr.emit(str(file_error))

        except:

            self.error_signal_kr.emit('Error occured. Written to error_info_kr.txt.')
            error_file = open('error_info_kr.txt', 'w')
            error_file.write(traceback.format_exc())
            error_file.close()
