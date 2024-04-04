# LLMBridge

LLMBridge is a Python utility designed to facilitate the integration of codebases with language learning models (LLMs) by consolidating multiple code files into a single document. This tool is particularly useful for developers looking to analyze or share their entire codebase in environments that support conversational models, such as ChatGPT. LLMBridge recursively traverses your project's directory structure, respects `.gitignore` exclusions, and filters files based on specified extensions in `.llmbridgeinclude`, preparing a comprehensive document ready for LLM interaction.

## Features

- **Recursive Directory Traversal**: Processes your entire project, including subdirectories, to capture every piece of code.
- **.gitignore Support**: Automatically skips files and directories specified in `.gitignore`, ensuring only relevant files are included.
- **Customizable Whitelist**: Utilizes a `.llmbridgeinclude` file to focus on specific file types, enhancing the model's understanding of your codebase.
- **Automatic `.llmbridgeinclude` Generation**: Generates a default whitelist if `.llmbridgeinclude` is missing, covering common coding file types.
- **Robust Error Handling**: Gracefully handles file access and encoding issues, ensuring a smooth operation.

## Getting Started

### Prerequisites

- Python 3.x installed on your system.
- pathspec library installed in your environment

### Installation

1. Clone this repository or download the script directly to your local machine.
2. Ensure `python` command is available in your system's PATH.

### Setup

Install `pathspec` external library for a more seamless implementation of .gitignore files

```bash
pip install pathspec
```

### Usage

Navigate to your project's directory and run LLMBridge using the following command:

```bash
python llmbridge.py <source_directory> <output_file_path>
```

Default Source Directory: The current directory (./) will be used if no source directory is provided.

Default Output File: LLMOutput.txt in the current directory will be used if no output file path is provided.

Replace `<source_directory>` with the path to your source directory and `<output_file_path>` with your custom output file path, if desired.

#### Example

```bash
python llmbridge.py
```

This command processes all files in the current directory (and its subdirectories) and writes the combined output to `LLMOutput.txt`.

## Configuration

### `.llmbridgeinclude`

To customize which file types are included, create or modify the `.llmbridgeinclude` file in your source directory root. Add one file extension per line, like so:

```
.py
.js
.html
.css
```

If `.llmbridgeinclude` is missing, LLMBridge will create one with a default set of common code file extensions.

### `.gitignore`

LLMBridge automatically respects `.gitignore` patterns. Ensure your `.gitignore` is configured to exclude any files or directories you do not wish to process.

## Contributing

Contributions to LLMBridge are welcome! Please feel free to submit pull requests, open issues, or suggest new features.

## License

This project is open source and available under the [MIT License](LICENSE).

## Future Additions

- Ideally I'd like to add in additional features, such as Diff formatting on subsequent runs, so if you modify your codebase that also gets passed to the LLM in a way that can identify introduced bugs, etc.