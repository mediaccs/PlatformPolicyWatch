# Policy Labeler

This Python script is designed to identify values (or other desired content) in a specified column from a csv file. 

# Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Walkthrough](#walkthrough)
  - [Step 1: Import Libraries](#step-1-import-necessary-libraries-and-function)
  - [Step 2: Provide API key](#step-2-provide-api-key)
  - [Step 3: Write a prompt](#step-3-write-a-prompt)
  - [Step 4: Provide your input file](#step-4-provide-your-input-file)
  - [Step 5: Run the model on the sample](#step-5-run-the-model-on-the-sample)


## Features
- Extract sample from policy sections.
- Label policy sections according to prompt.
- Output the lableled sections to a new Excel file.

## Prerequisites
- Python 3.x
- libraries (install using 'pip install *library*):

```python
pip3 install ast
pip3 install openai
pip3 install pandas
pip3 install os
pip3 install scripy
pip3 install re
```

- OpenAI api key

## Installation
Install libraries

## Walkthrough

### Step 1: Import necessary libraries and function
- Importing necessary Python libraries including pandas for data handling.


```python
import ast  # for converting embeddings saved as strings back to arrays
from openai import OpenAI # for calling the OpenAI API
import pandas as pd  # for storing text and embeddings data
import os # for getting API token from env variable OPENAI_API_KEY
from scipy import spatial  # for calculating vector similarities for search
import re  # for using regular expressions



```

### Step 2: Provide API key
- Retrive your API key from OpenAI. Note that making API calls might incure costs on your end.

```python
EMBEDDING_MODEL = "Enter your Embedding Model"
GPT_MODEL = "Enter Your ChatGPT Model"
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY","Enter Your Own API Key"))

```

### Step 3: Write a prompt
- Write your prompt. In this case, we are asking the model to identify whether any of these values (privacy, safety, and choice) are present in the section given to it. For each value, it is asked to respond with either 1 if the value is present or 0 if it is not present.


```python
questions = ['''Question 1.
            Please label if the section contains the following information.
            Return <1> if the information is present and <0> if the information is not present.
            Please identify the presence or not of all the asked information in the order they were asked.
            - Privacy: Privacy entails the degree to which users are empowered to manage their personal information, encompassing permissions for data control, sharing, and customization. It reflects the platform's approach in enabling or constraining user actions that influence the handling of their data, encapsulating transparency, consent, security, and user agency. 
            - Safety: Safety is defined as the freedom from danger or risk (Scharlach et al., 2023). It also includes advice on how to stay safe and descriptions of potential safety risks.
            - Choice: “Widely invoked in platform policies, choice signifies that individuals should be free to pick options that align with their interests. Through interface design, account personalization, and informational resources, platforms provide options and frame the ideal user as someone who makes active and informed choices that align with their preferences.” (Scharlach et al., 2023, p. 12). 
            Answer using this format, [0,0,0]. Do not provide any other information'''
]
```

   

### Step 4: Provide your input file
- Provide an input file (csv format).


```python
input_csv_path = "Your CSV File Name"
df = pd.read_csv(input_csv_path)
```


### Step 5: Run the model on the sample
- Run  the model on the sample and save the result in an csv file for you to review.


```python
# Ask ChatGPT to code
def ask_chatgpt(section_text, question):
    response = client.chat.completions.create(
     messages=[
        {"role": "system", "content": "You will answer questions about the policy."},
        {"role": "user", "content": f"{question}: {section_text}"}
     ],
     model=GPT_MODEL,
     temperature=0,
)

    return (response.choices[0].message.content)

# Process each row in the DataFrame
for index, row in df.iterrows():
    section_text = row['Section']
    for i, question in enumerate(questions, start=1):
        # Extract the first sentence of the question
        first_sentence = re.split(r'\.|\n', question)[0].strip()
        # Provide ChatGPT with the content from the CodeBook document
        response = ask_chatgpt(section_text, question)
        answer = response.split('\n')[-1]  # Extracting only the last response (answer to the question)
        df.loc[index, first_sentence] = answer  # Add the answer to the DataFrame


# Save the results to a new CSV file
output_csv_path = 'Enter Your Output Filename'
df.to_csv(output_csv_path, index=False)
```

