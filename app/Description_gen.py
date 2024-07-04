import os
from dotenv import load_dotenv
import pathlib
import textwrap

import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown


def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

load_dotenv()
api_key = os.getenv("API_KEY")


# Configure the genai library with the API key
genai.configure(api_key=api_key)
def generate_description(keywords:str):

    keywords_str = ", ".join(keywords)
    prompt = f"Using the following keywords: {keywords_str}, write a 2-3 line SEO-optimized description about an artisanal product."
    # Define the model and prompt
    model = genai.GenerativeModel('gemini-1.5-flash')

    response = model.generate_content(prompt)
    to_markdown(response.text)
    # Generate the content
    print(response.text)
    return response.text