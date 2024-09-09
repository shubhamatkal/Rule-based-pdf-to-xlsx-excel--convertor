import pdfplumber
import re
import pandas as pd

def pdf2csv(pdf_path, csv_path):
    # Define the header for the CSV file
    header = [
    "Bill_ID",
    "Branch",
    "V. No.",
    "Date",
    "Machine",
    "Biller",
    "Qty",
    "Number of entries",
    "Bill Amt.",
    "Product Code",
    "Product Name",
    "Quantity",
    "Shop-Rate",
    "MRP",
    "Amount"
    ]

    # Create an empty DataFrame with the header
    header_df = pd.DataFrame(columns=header)

    # Write the header DataFrame to a CSV file
    header_df.to_csv(csv_path, index=False, header=True)

    # Define the regular expressions for the patterns in the bill
    #using regex you can create your own set of rules to extract data from the pdf
    re_pattern_for_bill_entry = r"^(\d+)\s+([\w\s]+?)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+[\d.]+\s+[\d.]+$"
    re_bill_end_pattern = r"^Total Items:\s+\d+"
    re_pattern_new_bill = r"^BSNLROAD\s+\d+\s+\d{2}-\d{2}-\d{2}"
    current_bill = {}
    products = [] 

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            lines = text.split('\n')
            #here we are iterating over the lines of the pdf and extracting the data using regex
            for line in lines:
                if re.match(re_pattern_new_bill, line):
                    details = line.split()
                    day = details[2][:2]    # First two characters (dd)
                    month = details[2][3:5] # Characters from index 3 to 5 (mm)
                    bill_number = details[1]
                    bill_id = f"{day}{month}{bill_number}"
                    current_bill["id"] = bill_id
                    current_bill["Branch"] = details[0]
                    current_bill["V. No."] = details[1]
                    current_bill["Date"] = details[2]
                    current_bill["Machine"] = details[3]
                    current_bill["Biller"] = details[4]
                    current_bill["Qty"] = details[5]
                    current_bill["Entries"] = details[6]
                    current_bill["Bill Amt."] = details[7]
                    continue 

                if re.match(re_bill_end_pattern, line):
                    for product in products:
                        # Convert new data to DataFrame
                        new_df = pd.DataFrame([product])
                        # Append new data to the CSV file
                        new_df.to_csv(csv_path, mode='a', header=False, index=False)
                    current_bill = {}
                    products = []
                    continue

                match = re.match(re_pattern_for_bill_entry, line)
                if match:
                    item_code = match.group(1)
                    item_name = match.group(2).strip()
                    quantity = float(match.group(3))
                    shop_rate = float(match.group(4))
                    mrp = float(match.group(5))
                    amount = float(match.group(6))
                    products.append({
                        **current_bill,
                        "item_code": item_code, 
                        "item_name": item_name,
                        "quantity": quantity,
                        "shop_rate": shop_rate,
                        "mrp": mrp,
                        "amount": amount,
                    })

# Specify the paths
pdf_path = 'your_pdf.pdf'
csv_path = 'your_converted_file.csv'

# Extract data and save to csv
pdf2csv(pdf_path, csv_path)

print(f"PDF {pdf_path} has been converted to csv and saved as {csv_path}")
