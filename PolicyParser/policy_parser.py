import pandas as pd
import re

def process_ss_method(df, input_csv_filename, output_csv_filename):
    document_separator = "----"
    
    header = [field for field in df.columns if field != "Policy content"]
    rows = []

    for index, row in df.iterrows():
        if "Policy content" in row:
            document = row["Policy content"]
            if document:
                sections = document.split(document_separator)
                for section in sections:
                    if section.strip():
                        row_data = [row[field] for field in header]
                        row_data.append(section)
                        rows.append(row_data)

    sections_df = pd.DataFrame(rows, columns=header + ["Section"])
    sections_df.to_csv(output_csv_filename, index=False, encoding='utf-8')

def process_ms_method(df, input_csv_filename, output_csv_filename, separators, trigger_rows):
    header = [field for field in df.columns if field != "Policy content"] + ["Section"]
    all_sections = []

    # Initial separator index
    separator_idx = 0

    for index, row in df.iterrows():
        if "Policy content" in row:
            document = row["Policy content"]
            
            # Check if current row's "document number" is in the list of trigger rows
            if row["document number"].lower() in [tr.lower() for tr in trigger_rows]:
                # If there's a next separator, shift to it
                if separator_idx < len(separators) - 1:
                    separator_idx += 1

            # Split the document based on the current separator
            if separator_idx == 0:  # Use simple string split for the first separator for backward compatibility
                sections = document.split(separators[separator_idx])
            else:
                sections = re.split(separators[separator_idx], document)
            
            for section in sections:
                if section.strip():
                    row_data = [row[field] for field in df.columns if field != "Policy content"] + [section.strip()]
                    all_sections.append(row_data)

    sections_df = pd.DataFrame(all_sections, columns=header)
    sections_df.to_csv(output_csv_filename, index=False, encoding='utf-8')

def main():
    # Ask user for input and output filenames
    input_csv_filename = input("Enter the input CSV filename: ")
    output_csv_filename = input("Enter the desired output CSV filename: ")

    # Define your list of separators and trigger rows
    separators = ["\\.", r'-----|={5,}']  # List of separators
    trigger_rows = ["ota85"]  # List of rows (based on "document number") where the separator changes to the next one

    # Read the input CSV into a DataFrame
    df = pd.read_csv(input_csv_filename)

    print("Choose a method:")
    print("1. Single Separator Method")
    print("2. Multiple Separators Method")
    choice = input("Enter your choice (1/2): ")

    if choice == "1":
        process_ss_method(df, input_csv_filename, output_csv_filename)
    elif choice == "2":
        process_ms_method(df, input_csv_filename, output_csv_filename, separators, trigger_rows)
    else:
        print("Invalid choice!")

if __name__ == "__main__":
    main()
