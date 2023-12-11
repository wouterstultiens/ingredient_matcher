import os

def list_files(startpath, excluded_dirs, excluded_files):
    file_structure = "Project File Structure:\n"
    for root, dirs, files in os.walk(startpath, topdown=True):
        dirs[:] = [d for d in dirs if d not in excluded_dirs]

        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * level
        file_structure += f"{indent}{os.path.basename(root)}/\n"
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            if f not in excluded_files:
                file_structure += f"{subindent}{f}\n"
    return file_structure

def write_file_contents(directory, formats, excluded_dirs, excluded_files, output_file):
    with open(output_file, 'w') as file:
        file.write(list_files(directory, excluded_dirs, excluded_files))
        file.write("\nContents of .py and .html Files:\n")

        for root, dirs, files in os.walk(directory):
            if any(excluded in root for excluded in excluded_dirs):
                continue

            for file_name in files:
                if file_name.endswith(tuple(formats)) and file_name not in excluded_files:
                    file_path = os.path.join(root, file_name)
                    file.write(f"\nFile: {file_path}\n\n")
                    with open(file_path, 'r') as f:
                        file.write(f.read())
                        file.write("\n\n")

def main():
    directory = '.'  # Current directory
    formats = ['.py', '.html']
    output_file = 'project_structure.txt'
    excluded_dirs = {'venv', '.git', '.idea', '__pycache__', 'recipe_scraper'}
    excluded_files = {'project_contents.py', 'project_contents.txt', 'add_recipes.py'}

    write_file_contents(directory, formats, excluded_dirs, excluded_files, output_file)

if __name__ == "__main__":
    main()
