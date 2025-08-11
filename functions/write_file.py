import os

#%% write_file function
def write_file(working_directory:str , file_path: str, content: str) -> str:

     # Get absolute paths
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    # Check if the target file path is in the working directory
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot write to  "{file_path}" as it is outside the permitted working directory'
    
    try:
        with open(abs_file_path,'w') as file:
            file.write(content)
    except Exception as e:
        return f'Error writing file "{file_path}": {e}'
    
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
# %%
