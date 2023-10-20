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
