# PolicyParser
This Python script is designed to process a CSV file containing policy documents and extract sections from the documents using one or more specified separators. It also provides the ability to switch separators based on specific trigger rows in the CSV.

# Table of Contents

1. [Prerequisites](#prerequisites)
2. [Features](#features) 
3. [Installation](#installation)
4. [Walkthrough](#walkthrough)
    - [Step 1: Import Libraries](#step-1-import-libraries)
    - [Steps 2 through 8](#steps-2-through-8)
    - [Step 9: Configure Separators and Trigger Rows](#step-9-configure-separators-and-trigger-rows)
    - [Step 10: Provide Input Data](#step-10-provide-input-data)
    - [Step 11: Run the Code](#step-11-run-the-code)
5. [Output for Two Separators](#output-for-two-separators)
6. [Version with a Single Separator](#version-with-a-single-separator)







### Prerequisites

- Python 3.x
- pandas library (Install using `pip install pandas`)

## Features

- Extract sections from policy documents.
- Switch separators based on specific trigger rows.
- Output the extracted sections to a new CSV file.



### Installation

- Install the pandas library if not already installed.


```python
pip install pandas
```

## Walkthrough
 ### Step 1: Import Libraries
 Importing necessary Python libraries, including pandas for data handling and re for regular expressions.


```python
import pandas as pd
import re
```

### Steps 2 through 8
See comments throughout code for information on how to modify the code according to your input document.


```python
# Steps 2 and 3: Define the 'process_method' function and extract Header Columns
def process_method(df, input_csv_filename, output_csv_filename, separators, trigger_rows):
    header = [field for field in df.columns if field != "Policy content"] + ["Section"]
    all_sections = []

    # Step 4: Initialize Separator Index
    separator_idx = 0

    for index, row in df.iterrows():
        if "Policy content" in row: #Change "Policy content" to the column that contains the relevant documents in your file.
            document = row["Policy content"]
            
            # Step 5: Check if the current row's "document number" matches any of the trigger rows. Change "document number" to the relevant column in your file.
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

    # Step 8: Create a New DataFrame
    sections_df = pd.DataFrame(all_sections, columns=header)
    sections_df.to_csv(output_csv_filename, index=False, encoding='utf-8')
    return sections_df
```

#### Step 9: Configure Separators and Trigger Rows

- Default separators and trigger rows are defined, but these can be adjusted as needed for your specific data. In this example there are two separators and the change from the first to the second separator happens in a row called "ota85".


```python
separators = ["\\.", r'-----|={5,}']  # List of separators
trigger_rows = ["ota85"]  # List of rows (based on "document number") where the separator changes to the next one
```

### Step 10: provide input data
You will be prompted to provide the following information:
1. **Input CSV Filename:** Enter the filename of the CSV file you want to process. For example: 'youtube_without_duplicates.csv'
2. **Output CSV Filename:** Enter the desired output filename where the extracted sections will be saved. For example: 'youtube_sectioned.csv'
3. After entering the input and output filenames, the script will process the data based on the specified configuration.
The script performs the following steps:
- It reads the input CSV file, extracts the "Policy content" column, and processes the data.
- It uses the specified separators to split the policy documents into sections, switching separators based on the trigger rows as configured.
- The extracted sections are saved to the output CSV file.


```python
input_csv_filename = input("Enter the input CSV filename: ")
output_csv_filename = input("Enter the desired output CSV filename: ")

```

### Step 11: Run the code


```python
df = pd.read_csv(input_csv_filename)
out_df = process_method(df, input_csv_filename, output_csv_filename, separators, trigger_rows)
```

### Output for two separators:


```python
print(out_df.head())
```

      document number    OTA date                 OTA time Platform  \
    0            ota1  2013-06-19  2013-06-19--19-19-52.md  YouTube   
    1            ota1  2013-06-19  2013-06-19--19-19-52.md  YouTube   
    2            ota1  2013-06-19  2013-06-19--19-19-52.md  YouTube   
    3            ota1  2013-06-19  2013-06-19--19-19-52.md  YouTube   
    4            ota1  2013-06-19  2013-06-19--19-19-52.md  YouTube   
    
       Type of document  Last updated  \
    0  terms_of_service  June 9, 2010   
    1  terms_of_service  June 9, 2010   
    2  terms_of_service  June 9, 2010   
    3  terms_of_service  June 9, 2010   
    4  terms_of_service  June 9, 2010   
    
                                                 Section  
    0                          Community Guidelines\r\n1  
    1  Your Acceptance\r\n1.  By using or visiting th...  
    2  Service\r\n1.  These Terms of Service apply to...  
    3  YouTube Accounts\r\n1.  In order to access som...  
    4  General Use of the Service—Permissions and Res...  


### Version with a single separator:
Notice how the list of rows is empty since the separator stays the same throughout the document.


```python
separators = ["----"]  # List of separators
trigger_rows = []  # List of rows (based on "document number") where the separator changes to the next one
input_csv_filename = input("Enter the input CSV filename: ")
output_csv_filename = input("Enter the desired output CSV filename: ")
df = pd.read_csv(input_csv_filename)
out_df = process_method(df, input_csv_filename, output_csv_filename, separators, trigger_rows)
print(out_df.head())
```

      document number    OTA date                 OTA time Platform  \
    0            ota1  2021-10-07  2021-10-07--17-30-24.md     Lyft   
    1            ota1  2021-10-07  2021-10-07--17-30-24.md     Lyft   
    2            ota1  2021-10-07  2021-10-07--17-30-24.md     Lyft   
    3            ota1  2021-10-07  2021-10-07--17-30-24.md     Lyft   
    4            ota1  2021-10-07  2021-10-07--17-30-24.md     Lyft   
    
       Type of document Effective   Last updated  \
    0  terms_of_service      none  April 1, 2021   
    1  terms_of_service      none  April 1, 2021   
    2  terms_of_service      none  April 1, 2021   
    3  terms_of_service      none  April 1, 2021   
    4  terms_of_service      none  April 1, 2021   
    
                                                 Section  
    0  Last Updated: April 1, 2021\r\nThese Terms of ...  
    1  -\r\nThe Lyft Platform provides a marketplace ...  
    2  -\r\nLyft reserves the right to modify the ter...  
    3  ---\r\nThe Lyft Platform may only be used by i...  
    4  ---\r\nAs a Rider, you understand that request...  

