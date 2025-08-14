import os
from config import MAXCHARS
from google.genai import types
from functions.utils import get_validated_absolute_path

#%% get_file_content function
def get_file_contents(working_directory: str, file_path: str) -> str:
    try:
        abs_file_path = get_validated_absolute_path(working_directory, file_path, is_dir=False)
    except ValueError as e:
        return str(e)
    
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
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to get contents from, relative to the working directory. If not provided, return contents of file in the working directory itself.",
            ),
        },
        required=["file_path"],
    ),
)