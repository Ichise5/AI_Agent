# %% Imports
import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from functions.get_files_info import schema_get_files_info
from functions.get_file_contents import schema_get_file_contents
from functions.write_file import schema_write_file
from functions.run_python import schema_run_python_file



# %% 
def main():
    load_dotenv()

    varargin = sys.argv[1:]
    params = initial_setup()    
    if len(varargin) == 0:
        print("No prompt was supplied. The program will exit")
        exit(1)

    for value in varargin:
        if not value.startswith("--"):
            user_prompt = value
        if value == "--verbose":
            params["verbose"] = True

    if params["verbose"]:
        print(user_prompt)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_contents,
            schema_run_python_file,
            schema_write_file,

        ]
    )

    configuration=types.GenerateContentConfig(
        tools=[available_functions], system_instruction=system_prompt
    )
    
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    #print("available_functions:", available_functions)
    #print("tools:", [available_functions])
    #print("type:", type(available_functions))
    #print("type tools:", type([available_functions]))

    response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents=messages,
    config=configuration,
    )

    function_call = response.function_calls
    if function_call:
        for function_call_part in function_call:
            if function_call_part:
                print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(response.text)
    

    if params["verbose"]:
        used_tokens(response.usage_metadata, user_prompt)



def used_tokens(metadata, user_prompt):
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {metadata.prompt_token_count}")
    print(f"Response tokens: {metadata.candidates_token_count}")


def initial_setup():
    params = {
        "verbose": False
    }
    return params

if __name__ == "__main__":
    main()
