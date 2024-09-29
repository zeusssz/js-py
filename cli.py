import argparse
import os
from translator import read_js_file, translate_js_to_py, write_py_file

def validate_path(file_path):
    if not os.path.exists(file_path):
        raise ValueError(f"The file {file_path} does not exist.")
    if not os.path.isfile(file_path):
        raise ValueError(f"The path {file_path} is not a file.")

def main():
    parser = argparse.ArgumentParser(description='Translate JavaScript code to Python.')
    parser.add_argument('input_file', help='Path to the input JavaScript file')
    parser.add_argument('output_file', help='Path to the output Python file')
    
    args = parser.parse_args()
    
    validate_path(args.input_file)
    
    js_code = read_js_file(args.input_file)
    py_code = translate_js_to_py(js_code)
    write_py_file(args.output_file, py_code)

if __name__ == '__main__':
    main()