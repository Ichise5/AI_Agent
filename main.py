# %% Imports
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys



# %% 
def main():
    varargin = sys.argv[1:]
    params = initial_setup()    
    if len(varargin) == 0:
        print("No prompt was supplied. The program will exit")
        exit(1)

    

    for value in varargin:
        match value:
            case "--verbose":
                params["verbose"] = True

    user_prompt = varargin[0]

    if params["verbose"]:
        print(user_prompt)


    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)


    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents=messages
    )

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
