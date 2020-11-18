
# Web scraping program to download e-paper from the newspaper provider Karavali Munjavu, and send it to an email.

from requests import get
from PIL import Image
from bs4 import BeautifulSoup
from datetime import date
from datetime import timedelta
from argparse import ArgumentParser
from os import makedirs
from os import path
from os import listdir
from os import environ
from os import remove
from shutil import rmtree
from img2pdf import convert
from time import sleep
from PDFMerger import merge_pdf_in_folder
from send_email import send_email_pdf
from sys import argv
from sys import exit

parser = ArgumentParser()
parser.add_argument("--directory", "-d", help = "choose directory location (desktop, documents, downloads or your own)", 
default='desktop', type=str.lower)
parser.add_argument("--mail", "-m", help="send mail", nargs='+')
parser.add_argument("--delete", "-del", help="delete previous day's files", action='store_true')
args = parser.parse_args()

pathToDirectory = args.directory
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
    yesterdayFile = pathToDirectory + '/Karavali Munjavu ' + dateYesterday

    if path.isfile(yesterdayFile):
        remove(yesterdayFile)

dateToday = date.today().strftime("%d-%m-%Y")

folderPathImg = pathToDirectory + '/Karavali Munjavu ' + dateToday
folderPathPdf = pathToDirectory + '/Karavali Munjavu pdf ' + dateToday
makedirs(folderPathImg)  # Make a folder in desktop with today's date.
makedirs(folderPathPdf)

try:
    url = 'http://www.karavalimunjavu.com/'
    res = get(url)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, 'lxml')

    # Downloading images.
    for images in soup.select('img[data-big]'):
        pageNo = path.basename(images.get('data-big'))[15:]
        imgFile = open(path.join(folderPathImg, pageNo), 'wb')
        imgDownload = get(url+images.get('data-big'), stream=True)
        fileSize = int(imgDownload.headers.get('Content-Length', None))
        progress = 0
        print(f'\nDownloading page {pageNo}')
        for data in imgDownload:
            imgFile.write(data)
            progress += len(data)
            percentage = int((progress / fileSize) * 100)
            print(f"'\r{percentage}", end='')
        imgFile.close()    

    # Converting images to pdf.
    print('\nConverting images to pdf')
    for page in listdir(folderPathImg):
        pdf_bytes = convert(Image.open(folderPathImg+'//'+page).filename)
        file = open(path.join(folderPathPdf, page[:-4] + '.pdf'), 'wb')
        file.write(pdf_bytes)
        file.close()
    print('Images converted to pdf.')

    rmtree(folderPathImg)  # Deleting folder containing images.

    merge_pdf_in_folder(folderPathPdf, pathToDirectory, 'Karavali Munjavu ' + str(dateToday))

    rmtree(folderPathPdf)  # Deleting folder containing pdfs.

    if recipientAddress:
        send_email_pdf(recipientAddress, [pathToDirectory + '/Karavali Munjavu '+ dateToday + '.pdf'],
                   subject='Karavali Munjavu Newspaper ' + dateToday)

except:
    rmtree(folderPathImg)
    rmtree(folderPathImg)