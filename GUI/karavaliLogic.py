"""Web scraping program to download e-paper from the newspaper provider Karavali Munjavu, and send it to an email. Edge
compatible version."""

from requests import get
from PIL import Image
from bs4 import BeautifulSoup
from datetime import date
from os import makedirs
from os import path
from os import listdir
from shutil import rmtree
from img2pdf import convert
from PDFMerger import merge_pdf_in_folder
from send_email import send_email_pdf


def karavali_download(directory_path, recipient_address_list):

    date_today = date.today().strftime("%d-%m-%Y")

    folder_path_img = directory_path + 'Karavali Munjavu ' + date_today
    folder_path_pdf = directory_path + 'Karavali Munjavu pdf ' + date_today
    makedirs(folder_path_img)  # Make a folder in desktop with today's date.
    makedirs(folder_path_pdf)

    url = 'http://www.karavalimunjavu.com/'
    res = get(url)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, 'lxml')

    # Downloading images.
    for images in soup.select('img[data-big]'):
        page_no = path.basename(images.get('data-big'))[15:]
        img_file = open(path.join(folder_path_img, page_no), 'wb')
        img_download = get(url+images.get('data-big'))
        print(f'Downloading page {page_no}')
        for chunk in img_download.iter_content(100000):
            img_file.write(chunk)
        img_file.close()

    # Converting images to pdf.
    print('Converting images to pdf')
    for page in listdir(folder_path_img):
        pdf_bytes = convert(Image.open(folder_path_img+'//'+page).filename)
        file = open(path.join(folder_path_pdf, page[:-4] + '.pdf'), 'wb')
        file.write(pdf_bytes)
        file.close()
    print('Images converted to pdf.')

    rmtree(folder_path_img)  # Deleting folder containing images.

    merge_pdf_in_folder(folder_path_pdf, 'C:/Users/Sammy/Desktop', 'Karavali Munjavu ' + str(date_today))

    rmtree(folder_path_pdf)  # Deleting folder containing pdfs.

    if recipient_address_list != ['']:
        send_email_pdf(recipient_address_list, [r'C:/Users/Sammy/Desktop/Karavali Munjavu '+date_today + '.pdf'],
                       subject='Karavali Munjavu Newspaper ' + date_today)
