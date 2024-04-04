import os
import pathspec

def create_default_llmbridgeinclude(include_file_path):
    """Create a .llmbridgeinclude file with default extensions if it doesn't exist."""
    default_extensions = [
        '.py', '.js', '.html', '.css', '.go', '.java', '.cpp', '.c', '.cs', '.php',
        '.rb', '.swift', '.ts', '.vue', '.json', '.xml', '.yml', '.md', '.sh'
    ]
    with open(include_file_path, 'w') as file:
        for ext in default_extensions:
            file.write(ext + '\n')

def get_included_extensions(include_file_path):
    """Ensure .llmbridgeinclude exists and parse it for included extensions."""
    if not os.path.exists(include_file_path):
        create_default_llmbridgeinclude(include_file_path)
    
    with open(include_file_path, 'r') as file:
        return [line.strip() for line in file if line.strip()]

def get_gitignore_spec(gitignore_file_path, script_name="llmbridge.py"):
    """Parse the .gitignore file and return a pathspec object, ensuring the script itself is ignored."""
    patterns = []
    if os.path.exists(gitignore_file_path):
        with open(gitignore_file_path, 'r') as file:
            patterns = [line.strip() for line in file if line.strip() and not line.startswith('#')]
    
    # Add the script name to the list of patterns to ensure it's ignored
    patterns.append(script_name)
    
    spec = pathspec.PathSpec.from_lines('gitwildmatch', patterns)
    return spec

def append_to_gitignore(gitignore_file_path, output_file_path):
    """Append the output file path to .gitignore if it's not already listed."""
    # Normalize the output file path to a relative path and ensure Unix-style slashes
    relative_output_path = os.path.relpath(output_file_path, start=os.path.dirname(gitignore_file_path))
    relative_output_path = relative_output_path.replace(os.sep, '/')

    # Check if .gitignore exists and read its content
    if os.path.exists(gitignore_file_path):
        with open(gitignore_file_path, 'r') as file:
            lines = [line.strip() for line in file]
    else:
        lines = []

    # Append the output file path to .gitignore if it's not already listed
    if relative_output_path not in lines:
        with open(gitignore_file_path, 'a') as file:
            # Ensure there's a newline at the end before appending
            if lines and not lines[-1].endswith('\n'):
                file.write('\n')
            file.write(f'{relative_output_path}\n')

def process_directory_recursive(directory_path, output_file_path, included_extensions, gitignore_spec, first_call=True):
    """Recursively process files in the directory based on the filters and write them to the output file."""
    if first_call:
        # Open the output file at the beginning of the recursion
        global outfile
        outfile = open(output_file_path, 'w', encoding='utf-8')
    
    entries = os.listdir(directory_path)
    
    for entry in entries:
        entry_path = os.path.join(directory_path, entry)
        relative_path = os.path.relpath(entry_path, start=os.path.dirname(output_file_path))
        
        # Skip if entry matches gitignore pattern
        if gitignore_spec and gitignore_spec.match_file(relative_path):
            continue

        if os.path.isdir(entry_path):
            # Recursively process directories
            process_directory_recursive(entry_path, output_file_path, included_extensions, gitignore_spec, False)
        elif any(entry.endswith(ext) for ext in included_extensions):
            # Process files matching included extensions
            try:
                with open(entry_path, 'r', encoding='utf-8') as readfile:
                    content = readfile.read()
                    outfile.write(f'---------------------------------\nFile: {relative_path}\n---------------------------------\n\n{content}\n\n')
            except Exception as e:
                print(f"Error processing file {entry_path}: {e}")

    if first_call:
        # Close the output file at the end of the recursion
        outfile.close()

if __name__ == "__main__":
    import sys
    
    directory_path = sys.argv[1] if len(sys.argv) > 1 else "./"
    output_file_path = sys.argv[2] if len(sys.argv) > 2 else "./LLMOutput.txt"
    include_file_path = os.path.join(directory_path, '.llmbridgeinclude')
    gitignore_file_path = os.path.join(directory_path, '.gitignore')
    # Add our output file to .gitignore to avoid exposing sensitive information
    # Also to avoid printing it out twice upon re-running LLMBridge.py
    append_to_gitignore(gitignore_file_path, output_file_path)

    included_extensions = get_included_extensions(include_file_path)
    gitignore_spec = get_gitignore_spec(gitignore_file_path)

    process_directory_recursive(directory_path, output_file_path, included_extensions, gitignore_spec)