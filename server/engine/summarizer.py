from concurrent.futures import ThreadPoolExecutor

import openai
import tiktoken
from setting import setting

# TO_DO
# https://colab.research.google.com/github/GoogleCloudPlatform/generative-ai/blob/main/language/examples/document-summarization/summarization_large_documents_langchain.ipynb#scrollTo=pjj2UZilDF4Q

openai.api_key = setting.OPENAI_API_KEY


def load_text(file_path):
    with open(file_path, "r") as file:
        return file.read()


def save_to_file(responses, output_file):
    with open(output_file, "w") as file:
        for response in responses:
            file.write(response + "\n")


# Change your OpenAI chat model accordingly


def call_openai_api(chunk, brief=False):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "Hello I am SummarizeBot. What can I help you?",
            },
            {
                "role": "user",
                "content": f""" Please provide a summary of the following text.
                                TEXT: {chunk}
                                SUMMARY:
                                """,
            },
        ],
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.5,
    )

    return response.choices[0]["message"]["content"].strip()


def call_openai_api_brief(chunk):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "Hello I am SummarizeBot. What can I help you?",
            },
            {
                "role": "user",
                "content": f""" Please provide a precise and concise summary of the following text with max word 100.
                                Summary must capture all important subjects as it will used to build knowledge graph.
                                TEXT: {chunk}
                                SUMMARY:
                                """,
            },
        ],
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.1,
    )

    return response.choices[0]["message"]["content"].strip()


def split_into_chunks(text, tokens=500):
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    words = encoding.encode(text)
    chunks = []
    for i in range(0, len(words), tokens):
        chunks.append(" ".join(encoding.decode(words[i : i + tokens])))
    return chunks


def process_chunks(input_file, output_file, brief=False):
    text = load_text(input_file)
    chunks = split_into_chunks(text)

    with ThreadPoolExecutor() as executor:
        if not brief:
            responses = list(executor.map(call_openai_api, chunks))
        else:
            responses = list(executor.map(call_openai_api_brief, chunks))

    save_to_file(responses, output_file)


def summarize(title, output_path="./data/summary"):
    input_file = f"data/raw/{title}/{title}.txt"
    output_file = f"{output_path}/{title}.txt"

    process_chunks(input_file, output_file)

    input_file = f"data/summary/{title}.txt"
    output_file = f"{output_path}/{title}_brief.txt"
    process_chunks(input_file, output_file, brief=True)
