
# Web scraping program to download e-paper from the newspaper provider Karavali Munjavu, and send it to an email. Edge
# compatible version.

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
import sys

if len(sys.argv) < 2:
    print('''Usage: karavali-dl.py [recipient-email-address 1] [recipient-email-address 2] [
          recipient-email-address n]''')
    sys.exit()
else:
    recipientAddress = sys.argv[1:]

dateToday = date.today().strftime("%d-%m-%Y")

folderPathImg = 'PATH/TO/FOLDER/Karavali Munjavu ' + dateToday
folderPathPdf = 'PATH/TO/FOLDER/Karavali Munjavu pdf ' + dateToday
makedirs(folderPathImg)  # Make a folder in desktop with today's date.
makedirs(folderPathPdf)

url = 'http://www.karavalimunjavu.com/'
res = get(url)
res.raise_for_status()
soup = BeautifulSoup(res.text, 'lxml')

# Downloading images.
for images in soup.select('img[data-big]'):
    pageNo = path.basename(images.get('data-big'))[15:]
    imgFile = open(path.join(folderPathImg, pageNo), 'wb')
    imgDownload = get(url+images.get('data-big'))
    print(f'Downloading page {pageNo}')
    for chunk in imgDownload.iter_content(100000):
        imgFile.write(chunk)
    imgFile.close()

# Converting images to pdf.
print('Converting images to pdf')
for page in listdir(folderPathImg):
    pdf_bytes = convert(Image.open(folderPathImg+'//'+page).filename)
    file = open(path.join(folderPathPdf, page[:-4] + '.pdf'), 'wb')
    file.write(pdf_bytes)
    file.close()
print('Images converted to pdf.')

rmtree(folderPathImg)  # Deleting folder containing images.

merge_pdf_in_folder(folderPathPdf, '#PATH/TO/FOLDER#', 'Karavali Munjavu ' + str(dateToday))

rmtree(folderPathPdf)  # Deleting folder containing pdfs.

send_email_pdf(recipientAddress, [r'#PATH/TO/FOLDER#/Karavali Munjavu '+dateToday + '.pdf'],
               subject='Karavali Munjavu Newspaper ' + dateToday)
