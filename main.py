# %% Imports
import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types


from prompts import system_prompt
from config import WORKING_DIRECTORY, MAXITER, MODEL

from functions.get_files_info import schema_get_files_info
from functions.get_file_contents import schema_get_file_contents
from functions.write_file import schema_write_file
from functions.run_python import schema_run_python_file

from functions.get_files_info import get_files_info
from functions.get_file_contents import get_file_contents
from functions.write_file import write_file
from functions.run_python import run_python_file



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

    for IDX in range(MAXITER):
        try:
            response = client.models.generate_content(
            model=MODEL,
            contents=messages,
            config=configuration,
            )
        except Exception as e:
            print(f"Error occured when obtaining response from model. Followin the error:\n{e}")

        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)

        function_call = response.function_calls
        if function_call:
            for function_call_part in function_call:
                if function_call_part:
                    #print(f"Calling function: {function_call_part.name}({function_call_part.args})")
                    function_call_result = call_function(function_call_part, verbose=params["verbose"])
        else:
            print("Final response:")
            print(response.text)
            break
        

        if params["verbose"]:
            used_tokens(response.usage_metadata, user_prompt)

        if function_call_result.parts[0].function_response.response:
            messages.append(types.Content(parts=function_call_result.parts, role="user"))
            if params["verbose"]:
                print(f"-> {function_call_result.parts[0].function_response.response}")
                
        else:
            raise Exception(f"""called function "{function_call_part.name}"didn't return anything""")

    if IDX == MAXITER-1:
         print(f"Maximum iterations ({MAXITER}) reached.")

def used_tokens(metadata, user_prompt: str) -> None:
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {metadata.prompt_token_count}")
    print(f"Response tokens: {metadata.candidates_token_count}")


def initial_setup() -> dict[str, bool]:
    params = {
        "verbose": False
    }
    return params

def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")


    match function_call_part.name:
        case "get_files_info":
            function_result = get_files_info(WORKING_DIRECTORY, **function_call_part.args)
        case "get_file_contents":
            function_result = get_file_contents(WORKING_DIRECTORY, **function_call_part.args)
        case "run_python_file":
            function_result = run_python_file(WORKING_DIRECTORY, **function_call_part.args)
        case "write_file":
            function_result = write_file(WORKING_DIRECTORY, **function_call_part.args)
        case _:
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_call_part.name,
                        response={"error": f"Unknown function: {function_call_part.name}"},
                    )
                ],
            )

    return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"result": function_result},
                )
            ],
        )
        
    return 0

if __name__ == "__main__":
    main()

# %%
