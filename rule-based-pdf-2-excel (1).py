import pdfplumber
import pandas as pd
import re
from openpyxl import Workbook


def process_bill_summaary_from_pdf(pdf_path):
    main_heading = ""
    sub_heading = ""
    data = []
    headers = None

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            #creating new lines for each line in pdfs
            lines = text.split('\n')
            for line in lines:
                ''' Rules can be validated here for each line, 
                you can use regular expression, string matching and other ways.'''

                if line.startswith('Shubham Atkal'):
                    main_heading = line
                    continue
                if line.startswith('Row which are to be added in table'):
                    data_ = re.split(r'\s', line.strip())
                    data.append(data_)
                    #this lines are to be added in each bill data table
                    continue
                else:
                    # printing other lines to console for debugging
                    print(line)

                #end of rules

    return headers, data, main_heading, sub_heading


def write_to_excel(headers, data, main_heading, sub_heading, sheet_title,
                   excel_path):
    # Create a new workbook and select the active worksheet
    wb = Workbook()
    ws = wb.active
    ws.title = sheet_title

    # Write the main heading
    ws.append([main_heading])

    # Write the sub heading
    ws.append([sub_heading])

    # Add an empty row
    ws.append([])

    # Write the headers
    ws.append(headers)

    # Write the data
    for row in data:
        ws.append(row)

    # Save the workbook
    wb.save(excel_path)


pdf_path = "./name-of-pdf-file.pdf"
excel_path = "output-file-name.xlsx"
sheet_title = "Bill Summary"

headers, data, main_heading, sub_heading = process_bill_summaary_from_pdf(
    pdf_path)

write_to_excel(headers, data, main_heading, sub_heading, sheet_title,
               excel_path)
