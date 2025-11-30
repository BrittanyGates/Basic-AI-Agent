# Basic AI Agent

This project contains an AI agent designed to interact with your system.

**IMPORTANT SECURITY WARNING:**

Due to the nature of the tools utilized by this AI agent, they are not perfectly secure. It is **strongly recommended**
that you **do not** give this AI agent direct access to your main operating system filesystem or any sensitive data. Run
this agent in an isolated, sandboxed environment to prevent potential security vulnerabilities.

## Usage

You can run the AI agent by executing the `main.py` script with a prompt as a command-line argument.

```bash
python main.py "Your prompt here"
```

For a more detailed output of the agent's actions, you can use the `--verbose` flag:

```bash
python main.py "Your prompt here" --verbose
```

### Example

Here's an example of how you can ask the agent to list the files in the `calculator` directory:

```bash
python main.py "List the files in the calculator directory"
```

## Available Tools

The AI agent has access to the following tools:

- **`get_files_info(directory: str = ".")`**: Lists the files and directories within a specified directory. If no
  directory is provided, it lists the contents of the current working directory.
- **`get_file_content(file_path: str)`**: Reads and returns the content of a specified file.
- **`run_python_file(file_path: str)`**: Executes a Python file and returns its output.
- **`write_file(file_path: str, content: str)`**: Writes content to a specified file.

The agent will decide which tool to use based on your prompt.