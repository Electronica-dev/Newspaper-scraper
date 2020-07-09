# Merge pdf files in a folder (which contains ONLY pdf files).

import PyPDF2
import os
from datetime import date
from natsort import natsorted

# Get date in a recognizable format.
dateToday = date.today().strftime("%d-%m-%Y")

merger = PyPDF2.PdfFileMerger()


def merge_pdf_in_folder(folder_path, output_path):
    pdf_list = os.listdir(folder_path)

    file = []  # Creating empty list to store the file paths.

    # Loop to add folder path to filenames.
    for pdf_file in pdf_list:
        file.append(folder_path + r'/' + pdf_file)

    file = natsorted(file)  # Sorting the file in a numerical order.

    for PDF in file:
        merger.append(PDF)

    # Opening the file with the name containing today's date.
    file_path = open(os.path.join(output_path, 'Prajavani ' + dateToday + '.pdf'), 'wb')

    merger.write(file_path)  # Writing to the file.

    file_path.close()
    merger.close()
