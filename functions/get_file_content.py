from config import MAX_CHARS
from google.genai import types
import os

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Lists the content in the files in the specified directory, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the file to read.",
            ),
        },
        required=["file_path"],
    ),
)


def get_file_content(working_directory: str, file_path: str):
    full_path = os.path.join(working_directory, file_path)
    absolute_full_path = os.path.abspath(full_path)
    absolute_working_dir = os.path.abspath(working_directory)

    # Boundary check
    if not (absolute_full_path == absolute_working_dir or absolute_full_path.startswith(absolute_working_dir + os.sep)):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    # File check
    if not os.path.isfile(absolute_full_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(absolute_full_path, "r") as file:
            file_content = file.read(MAX_CHARS + 1)
            if len(file_content) > MAX_CHARS:
                file_content = file_content[:MAX_CHARS] + f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                return file_content
            return file_content
    except Exception as e:
        return f"Error: {e}"
