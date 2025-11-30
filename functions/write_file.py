from google.genai import types
import os

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes to the specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the file to write to.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),
        },
        required=["file_path", "content"],
    ),
)


def write_file(working_directory: str, file_path: str, content: str):
    full_path = os.path.join(working_directory, file_path)
    absolute_full_path = os.path.abspath(full_path)
    absolute_working_dir = os.path.abspath(working_directory)

    # Boundary check
    if not (absolute_full_path == absolute_working_dir or absolute_full_path.startswith(absolute_working_dir + os.sep)):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    # File check
    directory_path = os.path.dirname(absolute_full_path)
    try:
        if directory_path and not os.path.exists(directory_path):
            os.makedirs(directory_path)
        with open(absolute_full_path, "w") as file:
            file.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"
