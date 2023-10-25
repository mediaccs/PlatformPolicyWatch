{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# PolicyParser\n",
    "This Python script is designed to process a CSV file containing policy documents and extract sections from the documents using one or more specified separators. It also provides the ability to switch separators based on specific trigger rows in the CSV.\n",
    "\n",
    "# Table of Contents\n",
    "\n",
    "1. [Prerequisites](#prerequisites)\n",
    "2. [Features](#features) \n",
    "3. [Installation](#installation)\n",
    "4. [Walkthrough](#walkthrough)\n",
    "    - [Step 1: Import Libraries](#step-1-import-libraries)\n",
    "    - [Steps 2 through 8](#steps-2-through-8)\n",
    "    - [Step 9: Configure Separators and Trigger Rows](#step-9-configure-separators-and-trigger-rows)\n",
    "    - [Step 10: Provide Input Data](#step-10-provide-input-data)\n",
    "    - [Step 11: Run the Code](#step-11-run-the-code)\n",
    "5. [Output for Two Separators](#output-for-two-separators)\n",
    "6. [Version with a Single Separator](#version-with-a-single-separator)\n",
    "\n",
    "\n",
    "\n",
    "\n",
    "\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Prerequisites\n",
    "\n",
    "- Python 3.x\n",
    "- pandas library (Install using `pip install pandas`)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Features\n",
    "\n",
    "- Extract sections from policy documents.\n",
    "- Switch separators based on specific trigger rows.\n",
    "- Output the extracted sections to a new CSV file.\n",
    "\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Installation\n",
    "\n",
    "- Install the pandas library if not already installed."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 20,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Requirement already satisfied: pandas in /Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-packages (2.1.1)\n",
      "Requirement already satisfied: numpy>=1.26.0 in /Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-packages (from pandas) (1.26.1)\n",
      "Requirement already satisfied: python-dateutil>=2.8.2 in /Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-packages (from pandas) (2.8.2)\n",
      "Requirement already satisfied: pytz>=2020.1 in /Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-packages (from pandas) (2023.3.post1)\n",
      "Requirement already satisfied: tzdata>=2022.1 in /Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-packages (from pandas) (2023.3)\n",
      "Requirement already satisfied: six>=1.5 in /Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-packages (from python-dateutil>=2.8.2->pandas) (1.16.0)\n",
      "\n",
      "\u001b[1m[\u001b[0m\u001b[34;49mnotice\u001b[0m\u001b[1;39;49m]\u001b[0m\u001b[39;49m A new release of pip is available: \u001b[0m\u001b[31;49m23.2.1\u001b[0m\u001b[39;49m -> \u001b[0m\u001b[32;49m23.3.1\u001b[0m\n",
      "\u001b[1m[\u001b[0m\u001b[34;49mnotice\u001b[0m\u001b[1;39;49m]\u001b[0m\u001b[39;49m To update, run: \u001b[0m\u001b[32;49mpip3 install --upgrade pip\u001b[0m\n",
      "Note: you may need to restart the kernel to use updated packages.\n"
     ]
    }
   ],
   "source": [
    "pip install pandas"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Walkthrough\n",
    " ### Step 1: Import Libraries\n",
    "    - Importing necessary Python libraries, including pandas for data handling and re for regular expressions."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 21,
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "import re"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Steps 2 through 8\n",
    "See comments throughout code for information on how to modify the code according to your input document."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 22,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Steps 2 and 3: Define the 'process_method' function and extract Header Columns\n",
    "def process_method(df, input_csv_filename, output_csv_filename, separators, trigger_rows):\n",
    "    header = [field for field in df.columns if field != \"Policy content\"] + [\"Section\"]\n",
    "    all_sections = []\n",
    "\n",
    "    # Step 4: Initialize Separator Index\n",
    "    separator_idx = 0\n",
    "\n",
    "    for index, row in df.iterrows():\n",
    "        if \"Policy content\" in row: #Change \"Policy content\" to the column that contains the relevant documents in your file.\n",
    "            document = row[\"Policy content\"]\n",
    "            \n",
    "            # Step 5: Check if the current row's \"document number\" matches any of the trigger rows. Change \"document number\" to the relevant column in your file.\n",
    "            if row[\"document number\"].lower() in [tr.lower() for tr in trigger_rows]:\n",
    "                # If there's a next separator, shift to it\n",
    "                if separator_idx < len(separators) - 1:\n",
    "                    separator_idx += 1\n",
    "\n",
    "            # Step 6: Split the Document\n",
    "            if separator_idx == 0:  # Use simple string split for the first separator for backward compatibility\n",
    "                sections = document.split(separators[separator_idx])\n",
    "            else:\n",
    "                sections = re.split(separators[separator_idx], document)\n",
    "            \n",
    "            # Step 7: Append Sections\n",
    "            for section in sections:\n",
    "                if section.strip():\n",
    "                    row_data = [row[field] for field in df.columns if field != \"Policy content\"] + [section.strip()]\n",
    "                    all_sections.append(row_data)\n",
    "\n",
    "    # Step 8: Create a New DataFrame\n",
    "    sections_df = pd.DataFrame(all_sections, columns=header)\n",
    "    sections_df.to_csv(output_csv_filename, index=False, encoding='utf-8')\n",
    "    return sections_df"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "#### Step 9: Configure Separators and Trigger Rows\n",
    "\n",
    "- Default separators and trigger rows are defined, but these can be adjusted as needed for your specific data. In this example there are two separators and the change from the first to the second separator happens in a row called \"ota85\"."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 23,
   "metadata": {},
   "outputs": [],
   "source": [
    "separators = [\"\\\\.\", r'-----|={5,}']  # List of separators\n",
    "trigger_rows = [\"ota85\"]  # List of rows (based on \"document number\") where the separator changes to the next one"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Step 10: provide input data\n",
    "You will be prompted to provide the following information:\n",
    "1. **Input CSV Filename:** Enter the filename of the CSV file you want to process. For example: 'youtube_without_duplicates.csv'\n",
    "2. **Output CSV Filename:** Enter the desired output filename where the extracted sections will be saved. For example: 'youtube_sectioned.csv'\n",
    "3. After entering the input and output filenames, the script will process the data based on the specified configuration.\n",
    "The script performs the following steps:\n",
    "- It reads the input CSV file, extracts the \"Policy content\" column, and processes the data.\n",
    "- It uses the specified separators to split the policy documents into sections, switching separators based on the trigger rows as configured.\n",
    "- The extracted sections are saved to the output CSV file."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 24,
   "metadata": {},
   "outputs": [],
   "source": [
    "input_csv_filename = input(\"Enter the input CSV filename: \")\n",
    "output_csv_filename = input(\"Enter the desired output CSV filename: \")\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Step 11: Run the code"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 25,
   "metadata": {},
   "outputs": [],
   "source": [
    "df = pd.read_csv(input_csv_filename)\n",
    "out_df = process_method(df, input_csv_filename, output_csv_filename, separators, trigger_rows)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Output for two separators:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 26,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "  document number    OTA date                 OTA time Platform  \\\n",
      "0            ota1  2013-06-19  2013-06-19--19-19-52.md  YouTube   \n",
      "1            ota1  2013-06-19  2013-06-19--19-19-52.md  YouTube   \n",
      "2            ota1  2013-06-19  2013-06-19--19-19-52.md  YouTube   \n",
      "3            ota1  2013-06-19  2013-06-19--19-19-52.md  YouTube   \n",
      "4            ota1  2013-06-19  2013-06-19--19-19-52.md  YouTube   \n",
      "\n",
      "   Type of document  Last updated  \\\n",
      "0  terms_of_service  June 9, 2010   \n",
      "1  terms_of_service  June 9, 2010   \n",
      "2  terms_of_service  June 9, 2010   \n",
      "3  terms_of_service  June 9, 2010   \n",
      "4  terms_of_service  June 9, 2010   \n",
      "\n",
      "                                             Section  \n",
      "0                          Community Guidelines\\r\\n1  \n",
      "1  Your Acceptance\\r\\n1.  By using or visiting th...  \n",
      "2  Service\\r\\n1.  These Terms of Service apply to...  \n",
      "3  YouTube Accounts\\r\\n1.  In order to access som...  \n",
      "4  General Use of the Service—Permissions and Res...  \n"
     ]
    }
   ],
   "source": [
    "print(out_df.head())"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Version with a single separator:\n",
    "Notice how the list of rows is empty since the separator stays the same throughout the document."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 27,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "  document number    OTA date                 OTA time Platform  \\\n",
      "0            ota1  2021-10-07  2021-10-07--17-30-24.md     Lyft   \n",
      "1            ota1  2021-10-07  2021-10-07--17-30-24.md     Lyft   \n",
      "2            ota1  2021-10-07  2021-10-07--17-30-24.md     Lyft   \n",
      "3            ota1  2021-10-07  2021-10-07--17-30-24.md     Lyft   \n",
      "4            ota1  2021-10-07  2021-10-07--17-30-24.md     Lyft   \n",
      "\n",
      "   Type of document Effective   Last updated  \\\n",
      "0  terms_of_service      none  April 1, 2021   \n",
      "1  terms_of_service      none  April 1, 2021   \n",
      "2  terms_of_service      none  April 1, 2021   \n",
      "3  terms_of_service      none  April 1, 2021   \n",
      "4  terms_of_service      none  April 1, 2021   \n",
      "\n",
      "                                             Section  \n",
      "0  Last Updated: April 1, 2021\\r\\nThese Terms of ...  \n",
      "1  -\\r\\nThe Lyft Platform provides a marketplace ...  \n",
      "2  -\\r\\nLyft reserves the right to modify the ter...  \n",
      "3  ---\\r\\nThe Lyft Platform may only be used by i...  \n",
      "4  ---\\r\\nAs a Rider, you understand that request...  \n"
     ]
    }
   ],
   "source": [
    "separators = [\"----\"]  # List of separators\n",
    "trigger_rows = []  # List of rows (based on \"document number\") where the separator changes to the next one\n",
    "input_csv_filename = input(\"Enter the input CSV filename: \")\n",
    "output_csv_filename = input(\"Enter the desired output CSV filename: \")\n",
    "df = pd.read_csv(input_csv_filename)\n",
    "out_df = process_method(df, input_csv_filename, output_csv_filename, separators, trigger_rows)\n",
    "print(out_df.head())"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.0"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
