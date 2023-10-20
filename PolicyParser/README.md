# Processing CSV with Pandas

In this Markdown document, we'll explain a Python script for processing a CSV file using the Pandas library. The script reads an input CSV file, splits its document column based on a custom separator, and stores the resulting sections in a new CSV file.

## Python Code

```python
import pandas as pd

## Define a function to process the CSV
def process_csv(input_csv_filename, output_csv_filename, document_column, document_separator):
    # Read the input CSV file into a pandas DataFrame
    df = pd.read_csv(input_csv_filename)

    ## Define the header for the output CSV (excluding the specified document column)
    header = [field for field in df.columns if field != document_column]

    ## Create a list to store the rows of the output DataFrame
    rows = []

    ## Iterate through the rows in the DataFrame
    for index, row in df.iterrows():
        if document_column in row:
            document = row[document_column]

            ## Check if the document is not None
            if document:
                ## Split the document content into sections based on the custom separator
                sections = document.split(document_separator)

                ## Append the sections with the same row data and original document
                for section in sections:
                    if section.strip():  ## Check if the section is not empty
                        row_data = [row[field] for field in header]
                        row_data.append(section)
                        rows.append(row_data)

    ## Create a new DataFrame with the combined sections
    sections_df = pd.DataFrame(rows, columns=header + ["Section"])

    ## Save the combined DataFrame to a new CSV file
    sections_df.to_csv(output_csv_filename, index=False, encoding='utf-8')

## Example usage:
input_csv_filename = 'document.csv'
output_csv_filename = 'document_sectioned.csv'
document_column = "column"
document_separator = "----"

process_csv(input_csv_filename, output_csv_filename, document_column, document_separator)

# Separator Switch: Splitting Document Sections from CSV Using Pandas and Regular Expressions

In this Markdown document, we will explain a Python script that splits document sections from a CSV file using the Pandas library and regular expressions. The script reads an input CSV file, determines the section separator dynamically based on the content of the document, and saves the sections to a new CSV file.

## Python Code

```python
import pandas as pd
import re

## Specify the input CSV file name (assuming it's in the current working directory)
input_csv_filename = 'document.csv'

## Specify the output CSV file name
output_csv_filename = 'document_sectioned.csv'

## Create a list to store the sections from all documents
all_sections = []

## Read the input CSV file into a pandas DataFrame
df = pd.read_csv(input_csv_filename)

## Define the header for the output CSV (excluding "the original text column")
header = [field for field in df.columns if field != "NAME OF ORIGINAL TEXT COLUMN"] + ["Section"]

## Variables to track if we've reached a document where the separator changes
reached_DOCUMENTNUMBERWHERESEPARATORCHANGES = False

## Specify the two document separators; adapt it to your document, here are 2 examples
document_separator = "\\."
document_separator2 = r'-----|={5,}'  ## Pattern to match 5 or more dashes or 5 or more equal signs

## Initialize the DataFrame with an empty 'Section' column
df["Section"] = ""

## Iterate through the rows in the DataFrame
for index, row in df.iterrows():
    if "NAME OF ORIGINAL TEXT COLUMN" in row:
        document = row["NAME OF ORIGINAL TEXT COLUMN"]

        ## Check if the document number is the one where the separator changes (in lowercase)
        if row["document number"].lower() == "DOCUMENT NUMBER WHERE SEPARATOR CHANGES":
            reached_DOCUMENTNUMBERWHERESEPARATORCHANGES = True

        ## Use the appropriate separator based on whether we've reached the document where the separator changes
        if reached_DOCUMENTNUMBERWHERESEPARATORCHANGES:
            document_separator = document_separator2

        ## Split the document content into sections based on the separator
        sections = document.split(document_separator) if not reached_DOCUMENTNUMBERWHERESEPARATORCHANGES else re.split(document_separator2, document)

        ## Append the sections with the same row data and the original document
        for section in sections:
            if section.strip():  ## Check if the section is not empty
                row_data = [row[field] for field in header]
                row_data[-1] = section.strip()
                all_sections.append(row_data)

## Create a new DataFrame with the combined sections
output_df = pd.DataFrame(all_sections, columns=header)

## Save the combined DataFrame to a new CSV file
output_df.to_csv(output_csv_filename, index=False, encoding='utf-8')


# Separator Switch: Splitting Document Sections from CSV Using Pandas and Regular Expressions

In this Markdown document, we will explain a Python script that splits document sections from a CSV file using the Pandas library and regular expressions. The script reads an input CSV file, determines the section separator dynamically based on the content of the document, and saves the sections to a new CSV file.

## Python Code

```python
import pandas as pd
import re

## Specify the input CSV file name (assuming it's in the current working directory)
input_csv_filename = 'document.csv'

## Specify the output CSV file name
output_csv_filename = 'document_sectioned.csv'

## Create a list to store the sections from all documents
all_sections = []

## Read the input CSV file into a pandas DataFrame
df = pd.read_csv(input_csv_filename)

## Define the header for the output CSV (excluding "the original text column")
header = [field for field in df.columns if field != "NAME OF ORIGINAL TEXT COLUMN"] + ["Section"]

## Variables to track if we've reached a document where the separator changes
reached_DOCUMENTNUMBERWHERESEPARATORCHANGES = False

## Specify the two document separators; adapt it to your document, here are 2 examples
document_separator = "\\."
document_separator2 = r'-----|={5,}'  ## Pattern to match 5 or more dashes or 5 or more equal signs

## Initialize the DataFrame with an empty 'Section' column
df["Section"] = ""

## Iterate through the rows in the DataFrame
for index, row in df.iterrows():
    if "NAME OF ORIGINAL TEXT COLUMN" in row:
        document = row["NAME OF ORIGINAL TEXT COLUMN"]

        ## Check if the document number is the one where the separator changes (in lowercase)
        if row["document number"].lower() == "DOCUMENT NUMBER WHERE SEPARATOR CHANGES":
            reached_DOCUMENTNUMBERWHERESEPARATORCHANGES = True

        ## Use the appropriate separator based on whether we've reached the document where the separator changes
        if reached_DOCUMENTNUMBERWHERESEPARATORCHANGES:
            document_separator = document_separator2

        ## Split the document content into sections based on the separator
        sections = document.split(document_separator) if not reached_DOCUMENTNUMBERWHERESEPARATORCHANGES else re.split(document_separator2, document)

        ## Append the sections with the same row data and the original document
        for section in sections:
            if section.strip():  ## Check if the section is not empty
                row_data = [row[field] for field in header]
                row_data[-1] = section.strip()
                all_sections.append(row_data)

## Create a new DataFrame with the combined sections
output_df = pd.DataFrame(all_sections, columns=header)

## Save the combined DataFrame to a new CSV file
output_df.to_csv(output_csv_filename, index=False, encoding='utf-8')

