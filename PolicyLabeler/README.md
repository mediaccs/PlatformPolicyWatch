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
  - [Step 6: Review and fine-tuning](#step-6-review-and-fine-tuning)


## Features
- Extract sample from policy sections.
- Label policy sections according to prompt.
- Output the lableled sections to a new Excel file.

## Prerequisites
- Python 3.x
- libraries (install using 'pip install *library*):
    - pandas, openai, ast, re, os, scripy
- OpenAI api key

## Installation
Install libraries

## Walkthrough

### Step 1: Import necessary libraries and function
- Importing necessary Python libraries including pandas for data handling.


```python
pip3 install ast
pip3 install openai
pip3 install pandas
pip3 install os
pip3 install scripy
pip3 install re

```

### Step 2: Provide API key
- Retrive your API key from OpenAI. Note that making API calls might incure costs on your end.

```python
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY","Enter Your Own API Key"))

```

### Step 3: Write a prompt
- Write your prompt. In this case, we are asking the model to identify whether any of these values (privacy, safety, and choice) are present in the section given to it. For each value, it is asked to respond with either 1 if the value is present or 0 if it is not present.


```python
questions = []
```

   

### Step 4: Provide your input file
- Provide an input file (csv format).


```python
input_csv_path = "Your CSV File Name"
de = pd.read_csv(input_csv_path)
```

![image](https://github.com/mediaccs/PlatformPolicyWatch/assets/131724876/a2044f15-b9f1-44b5-a5ea-34057b47c9ff)



### Step 5: Run the model on the sample
- Run  the model on the sample and save the result in an xlsx file for you to review.


```python
# Q3 initial sample 

if __name__ == "__main__":
    # Setup parameters
    column_name = "Section"  # the column name for the text to be classified
    model_name = "gpt-4"  # the GPT model to use
    label_num = 3  # the number of dimensions of this variable
    valid_values = ['0', '1']  # the valid answers from this question
    temperature = 0.7  # temperature 
    q_name = "Q3"  # the name of this question/variable
    once_verify_num = 3  # the numbers of results generated from GPT 
    max_verify_retry = 5  # the number of retries if the previous is not converged
    prompt = prompt_Q3

    # Initialize GPT Classifier
gpt_classifier = GPTClassifier()

    # Setup classification task
classification_task = ClassificationTask(
        column=column_name,
        prompt=prompt,
        model_name=model_name,
        label_num=label_num,
        valid_values=valid_values,
        temperature=temperature,
        q_name=q_name,
        once_verify_num=once_verify_num,
        max_verify_retry=max_verify_retry
    )

    # Classify and save the result
result_df_q3_first_try = gpt_classifier.classify_df(Q3_initial_sample, classification_task)
result_df_q3_first_try.to_excel("classification_output.xlsx") #change name to desired output file
```

   



```python
result_df_q3_first_try
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Unnamed: 0</th>
      <th>document number</th>
      <th>OTA date</th>
      <th>OTA time</th>
      <th>Platform</th>
      <th>Type of document</th>
      <th>Effective</th>
      <th>Last updated</th>
      <th>Section</th>
      <th>Q3_1_classification</th>
      <th>Q3_2_classification</th>
      <th>Q3_3_classification</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0</td>
      <td>ota1</td>
      <td>2021-10-07</td>
      <td>2021-10-07--17-30-24.md</td>
      <td>Lyft</td>
      <td>terms_of_service</td>
      <td>none</td>
      <td>2021-04-01</td>
      <td>Last Updated: April 1, 2021_x000D_\nThese Term...</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>ota1</td>
      <td>2021-10-07</td>
      <td>2021-10-07--17-30-24.md</td>
      <td>Lyft</td>
      <td>terms_of_service</td>
      <td>none</td>
      <td>2021-04-01</td>
      <td>-_x000D_\nThe Lyft Platform provides a marketp...</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2</td>
      <td>ota1</td>
      <td>2021-10-07</td>
      <td>2021-10-07--17-30-24.md</td>
      <td>Lyft</td>
      <td>terms_of_service</td>
      <td>none</td>
      <td>2021-04-01</td>
      <td>-_x000D_\nLyft reserves the right to modify th...</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>3</td>
      <td>ota1</td>
      <td>2021-10-07</td>
      <td>2021-10-07--17-30-24.md</td>
      <td>Lyft</td>
      <td>terms_of_service</td>
      <td>none</td>
      <td>2021-04-01</td>
      <td>---_x000D_\nThe Lyft Platform may only be used...</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>4</td>
      <td>ota1</td>
      <td>2021-10-07</td>
      <td>2021-10-07--17-30-24.md</td>
      <td>Lyft</td>
      <td>terms_of_service</td>
      <td>none</td>
      <td>2021-04-01</td>
      <td>---_x000D_\nAs a Rider, you understand that re...</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
    </tr>
    <tr>
      <th>5</th>
      <td>5</td>
      <td>ota1</td>
      <td>2021-10-07</td>
      <td>2021-10-07--17-30-24.md</td>
      <td>Lyft</td>
      <td>terms_of_service</td>
      <td>none</td>
      <td>2021-04-01</td>
      <td>_x000D_\nIf you are a Driver, you will receive...</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>6</th>
      <td>6</td>
      <td>ota1</td>
      <td>2021-10-07</td>
      <td>2021-10-07--17-30-24.md</td>
      <td>Lyft</td>
      <td>terms_of_service</td>
      <td>none</td>
      <td>2021-04-01</td>
      <td>---_x000D_\nBy entering into this Agreement or...</td>
      <td>1</td>
      <td>0</td>
      <td>1</td>
    </tr>
    <tr>
      <th>7</th>
      <td>7</td>
      <td>ota1</td>
      <td>2021-10-07</td>
      <td>2021-10-07--17-30-24.md</td>
      <td>Lyft</td>
      <td>terms_of_service</td>
      <td>none</td>
      <td>2021-04-01</td>
      <td>_x000D_\nYour Information is any information y...</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>8</th>
      <td>8</td>
      <td>ota1</td>
      <td>2021-10-07</td>
      <td>2021-10-07--17-30-24.md</td>
      <td>Lyft</td>
      <td>terms_of_service</td>
      <td>none</td>
      <td>2021-04-01</td>
      <td>---_x000D_\nLyft, at its sole discretion, may ...</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
    </tr>
    <tr>
      <th>9</th>
      <td>9</td>
      <td>ota1</td>
      <td>2021-10-07</td>
      <td>2021-10-07--17-30-24.md</td>
      <td>Lyft</td>
      <td>terms_of_service</td>
      <td>none</td>
      <td>2021-04-01</td>
      <td>-_x000D_\nWith respect to your use of the Lyft...</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
</div>



### Step 6: Review and fine-tuning
- Review and fine tune your model. For more information see https://github.com/mediaccs/LabelGenius .
