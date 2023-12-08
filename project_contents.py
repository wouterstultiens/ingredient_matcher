import os

def list_files(startpath, excluded_dirs):
    file_structure = ""
    for root, dirs, files in os.walk(startpath, topdown=True):
        # Remove excluded directories from traversal
        dirs[:] = [d for d in dirs if d not in excluded_dirs]

        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * level
        file_structure += '{}{}/\n'.format(indent, os.path.basename(root))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            file_structure += '{}{}\n'.format(subindent, f)
    return file_structure

def main():
    directory = '.'  # Current directory
    output_file = 'project_structure.txt'
    excluded_dirs = {'venv', '.git', '.idea', '__pycache__'}  # Directories to exclude

    with open(output_file, 'w') as file:
        file.write("Project File Structure:\n")
        file.write(list_files(directory, excluded_dirs))
        file.write("\nContents of .py and .html Files:\n")

        for root, dirs, files in os.walk(directory):
            # Skip excluded directories
            if any(excluded in root for excluded in excluded_dirs):
                continue

            for file_name in files:
                if file_name.endswith('.py') or file_name.endswith('.html'):
                    file_path = os.path.join(root, file_name)
                    file.write(f"\nFile: {file_path}\n\n")
                    with open(file_path, 'r') as f:
                        contents = f.read()
                        file.write(contents)
                        file.write("\n\n")

if __name__ == "__main__":
    main()