import os
from config import MAXCHARS
from google.genai import types

#%% get_file_content function
def get_file_content(working_directory: str, file_path: str) -> str:

    # Get absolute paths
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    # Check if the target file path is in the working directory
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    # Check if the target file is a file
    if not os.path.isfile(abs_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    # Read the contents of the file
    try:
        with open(abs_file_path, "r") as f:
            content = f.read(MAXCHARS)
            # If the file is bigger than MAXCHARS return add a notation to the end
            if os.path.getsize(abs_file_path) > MAXCHARS:
                content += (
                    f'[...File "{file_path}" truncated at {MAXCHARS} characters]'
                )
        return content
    #If anything goes wrong return error
    except Exception as e:
        return f'Error reading file "{file_path}": {e}'
    
# %%

schema_get_file_contents = types.FunctionDeclaration(
    name="get_file_contents",
    description=f"Lists contents of a file in the specified directory up to limiting amount of characters to {MAXCHARS} which will be denoted, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file": types.Schema(
                type=types.Type.STRING,
                description="The file to get contents from, relative to the working directory. If not provided, return contents of file in the working directory itself.",
            ),
        },
        required=["file_path"],
    ),
)