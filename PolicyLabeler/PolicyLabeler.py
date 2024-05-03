# imports
import ast  # for converting embeddings saved as strings back to arrays
from openai import OpenAI # for calling the OpenAI API
import pandas as pd  # for storing text and embeddings data
import os # for getting API token from env variable OPENAI_API_KEY
from scipy import spatial  # for calculating vector similarities for search
import re  # for using regular expressions


# models
EMBEDDING_MODEL = "Enter your Embedding Model"
GPT_MODEL = "Enter Your ChatGPT Model"
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY","Enter Your Own API Key"))


# List of questions to be asked based on the "Section" column
questions = []

# Load the input CSV file
input_csv_path = "Your CSV File Name"
df = pd.read_csv(input_csv_path)

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