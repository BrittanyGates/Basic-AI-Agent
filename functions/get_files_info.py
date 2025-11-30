from google.genai import types
from .get_file_content import schema_get_file_content
from .run_python_file import schema_run_python_file
from .write_file import schema_write_file
import os

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)

def get_files_info(working_directory, directory="."):
    full_path = os.path.join(working_directory, directory)
    absolute_full_path = os.path.abspath(full_path)
    absolute_working_dir = os.path.abspath(working_directory)

    # Boundary check
    if not absolute_full_path.startswith(absolute_working_dir):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    # Directory check
    if not os.path.isdir(absolute_full_path):
        return f'Error: "{directory}" is not a directory'

    directory_contents = os.listdir(absolute_full_path)
    contents = []

    try:
        for item in directory_contents:
            item_path = os.path.join(absolute_full_path, item)
            item_size = os.path.getsize(item_path)
            is_dir = os.path.isdir(item_path)
            contents.append(f"- {item}: file_size={item_size} bytes, is_dir={is_dir}")
        return "\n".join(contents)
    except Exception as e:
        return f"Error: {e}"
