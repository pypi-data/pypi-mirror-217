"""DashIQ chat methods"""

import os
import openai
from dotenv import load_dotenv
from dashiqlib import MissingEnvVarException

load_dotenv()

MAIN_PROMPT_PREFIX = """
Write a function in Python called "answer_question" that always accepts 1 argument: A Pandas DataFrame. The function always returns as answer as a string.
Use the input Dataframe to best answer the question. 
If you need to generate a plot in order to answer the question, please use the seaborn library and set the style to "darkgrid" using "sns.set_style('darkgrid')"
and save the image to the current working directory and include the file name in the return string. 

Do not forget to import the libraries you need (i.e. if you need seaborn). 
In your response, only include the Python code or Python comments. Do not include any text other than Python code (no "```python" for example).
Only include Python code in your response. Do not include example usage in your response. Only provide to Python function and nothing more.
Don't forget all necessary imports.

If you need to use plt import it with: "from matplotlib import pyplot as plt"

The DataFrame will have the following column names and data types. The column names describe the data contained in the respective column of the DataFrame:
_id                              object
_sdc_primary_key                 object
adGroup.resourceName             object
adGroup.id                       object
campaign.resourceName            object
campaign.id                      object
metrics.clicks                    int64
metrics.costMicros                int64
metrics.impressions               int64
segments.date            datetime64[ns]
campaign.name                    object


Here is the user's question:
"""


def generate_python(workspace_dir: str, q: str):
    """A Python function that generates python code to a specified workspace direcrtory"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise MissingEnvVarException
    openai.api_key = api_key
    completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            temperature=0,
            messages=[{"role": "user", "content": MAIN_PROMPT_PREFIX + q}])
    code = completion.choices[0].message.content

    # clean up if it needs it
    code = str(code).replace("```python", '')
    code = code.replace("```", '')

    with open(workspace_dir + 'answer.py', 'w', encoding='UTF-8') as file:
        file.write(code)
