import pandas as pd
import re

# Specify the input CSV file name (assuming it's in the current working directory)
input_csv_filename = 'document.csv'

# Specify the output CSV file name
output_csv_filename = 'document_sectioned.csv'

# Create a list to store the sections from all documents
all_sections = []

# Read the input CSV file into a pandas DataFrame
df = pd.read_csv(input_csv_filename)

# Define the header for the output CSV (excluding "the original text column" - the goal is to minimize the file size by not including the original policy text)
header = [field for field in df.columns if field != "NAME OF ORIGINAL TEXT COLUMN"] + ["Section"]

# Variables to track if we've reached document where the separator changes
reached_DOCUMENTNUMBERWHERESEPARATORCHANGES = False

# Specify the two document separators adapt it to your document, here are 2 examples
document_separator = "\\."
document_separator2 = r'-----|={5,}'  # Pattern to match 5 or more dashes or 5 or more equal signs

# Initialize the DataFrame with an empty 'Section' column
df["Section"] = ""

# Iterate through the rows in the DataFrame
for index, row in df.iterrows():
    if "NAME OF ORIGINAL TEXT COLUMN" in row:
        document = row["NAME OF ORIGINAL TEXT COLUMN"]

        # Check if the document number is the one where the separator changes (in lowercase)
        if row["document number"].lower() == "DOCUMENT NUMBER WHERE SEPARATOR CHANGES":
            reached_DOCUMENTNUMBERWHERESEPARATORCHANGES = True

        # Use the appropriate separator based on whether we've reached DOCUMENT NUMBRE WHERE SEPARATOR CHANGES
        if reached_DOCUMENTNUMBERWHERESEPARATORCHANGES:
            document_separator = document_separator2

        # Split the document content into sections based on the separator
        sections = document.split(document_separator) if not reached_DOCUMENTNUMBERWHERESEPARATORCHANGES else re.split(document_separator2, document)

        # Append the sections with the same row data and original document
        for section in sections:
            if section.strip():  # Check if the section is not empty
                row_data = [row[field] for field in header]
                row_data[-1] = section.strip()
                all_sections.append(row_data)

# Create a new DataFrame with the combined sections
output_df = pd.DataFrame(all_sections, columns=header)

# Save the combined DataFrame to a new CSV file
output_df.to_csv(output_csv_filename, index=False, encoding='utf-8')
