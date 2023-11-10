# Step 1: Import Libraries
import pandas as pd
import re

# Steps 2 and 3: Define the 'process_method' function and extract Header Columns
def process_method(df, input_csv_filename, output_csv_filename, separators, trigger_rows):
    # Step 4: Initialize Separator Index
    header = [field for field in df.columns if field != "Policy content"] + ["Section"]
    all_sections = []
    separator_idx = 0

    for index, row in df.iterrows():
        if "Policy content" in row: #Change "Policy content" to the column that contains the relevant documents in your file.
            document = row["Policy content"]

            # Step 5: Check if current row's "document number" is in the list of trigger rows. Change "document number" to the relevant name in your csv file.

            if row["document number"].lower() in [tr.lower() for tr in trigger_rows]:
                # If there's a next separator, shift to it
                if separator_idx < len(separators) - 1:
                    separator_idx += 1

            # Step 6: Split the Document
            if separator_idx == 0:  # Use simple string split for the first separator for backward compatibility
                sections = document.split(separators[separator_idx])
            else:
                sections = re.split(separators[separator_idx], document)

            # Step 7: Append Sections
            for section in sections:
                if section.strip():
                    row_data = [row[field] for field in df.columns if field != "Policy content"] + [section.strip()]
                    all_sections.append(row_data)

    # Step 8: Create a New DataFrame and add column that adds a unique index for each section
    sections_df = pd.DataFrame(all_sections, columns=header)
    sections_df.insert(1, "Section Index", sections_df["document number"] + "_" + sections_df.groupby("document number").cumcount().add(1).astype(str)) 
    sections_df.to_csv(output_csv_filename, index=False, encoding='utf-8')
    return sections_df



def main():
    # Step 9: Configure Separators and Trigger Rows
    separators = ["\\.", r'-----|={5,}']  # List of separators in order of appearance
    trigger_rows = ["ota85"]  # List of rows (based on "document number") where the separator changes to the next one
    # Step 10: Provide input data
    input_csv_filename = input("Enter the input CSV filename: ")
    output_csv_filename = input("Enter the desired output CSV filename: ")

    # Step 11: Run the code
    df = pd.read_csv(input_csv_filename)
    out_df = process_method(df, input_csv_filename, output_csv_filename, separators, trigger_rows)

if __name__ == "__main__":
    main()
