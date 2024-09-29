import re

def read_js_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def translate_js_to_py(js_code):
    py_code = re.sub(r'\bvar\b|\blet\b|\bconst\b', '', js_code)
    py_code = re.sub(r'function\s+(\w+)\s*\((.*?)\)\s*{', r'def \1(\2):', py_code)
    py_code = re.sub(r'console\.log', 'print', py_code)
    py_code = re.sub(r';', '', py_code)
    indentation_level = 0
    py_code_lines = []

    for line in py_code.splitlines():
        line = line.strip()
        if line.endswith('{'):
            indentation_level += 1
            line = line[:-1]
        elif line == '}':
            indentation_level -= 1
            continue
        py_code_lines.append('    ' * indentation_level + line)

    py_code = '\n'.join(py_code_lines)
    py_code = re.sub(r'if\s*\((.*?)\)\s*:', r'if \1:', py_code)
    py_code = re.sub(r'else\s*{', 'else:', py_code)
    py_code = re.sub(r'else\s+if\s*\((.*?)\)\s*{', r'elif \1:', py_code)
    py_code = re.sub(r'for\s*\((.*?);(.*?);(.*?)\)\s*:', r'for \1 in range(\2, \3):', py_code)
    py_code = re.sub(r'for\s*\(let\s+(\w+)\s+of\s+(.*?)\)\s*{', r'for \1 in \2:', py_code)
    py_code = re.sub(r'while\s*\((.*?)\)\s*:', r'while \1:', py_code)
    py_code = re.sub(r'do\s*{(.*?)}\s*while\s*\((.*?)\);', r'while \2:\n    \1', py_code, flags=re.DOTALL)
    py_code = re.sub(r'\[(.*?)\]', r'[\1]', py_code)
    py_code = re.sub(r'{\s*(.*?):\s*(.*?)\s*}', r'{\1: \2}', py_code)
    py_code = re.sub(r'return\s+(.*?);', r'return \1', py_code)
    py_code = re.sub(r'===?', '==', py_code)
    py_code = re.sub(r'!==?', '!=', py_code)
    py_code = re.sub(r'(.*?)\?\s*(.*?):\s*(.*)', r'\1 if \2 else \3', py_code)
    py_code = re.sub(r'(\w+)\s*=\s*function\s*\((.*?)\)\s*{', r'\1 = lambda \2:', py_code)
    py_code = re.sub(r'(\w+)\.push\((.*?)\);?', r'\1.append(\2)', py_code)
    py_code = re.sub(r'(\w+)\.pop\(\);?', r'\1.pop()', py_code)
    py_code = re.sub(r'(\w+)\s*\+\s*(\w+)', r'\1 + \2', py_code)
    py_code = re.sub(r'async\s+function\s+(\w+)\s*\((.*?)\)\s*{', r'def \1(\2):\n    pass  # Async functions not fully translated', py_code)
    py_code = re.sub(r'await\s+', '', py_code)
    py_code = re.sub(r'new\s+Promise\((.*?)\)\s*{', r'Promise(\1):', py_code)
    py_code = re.sub(r'try\s*{', r'try:', py_code)
    py_code = re.sub(r'catch\s*\((.*?)\)\s*{', r'except \1:', py_code)
    py_code = re.sub(r'switch\s*\((.*?)\)\s*{', r'def switch_case(\1):\n    return {', py_code)
    py_code = re.sub(r'case\s+(.*?):', r'    \1: ', py_code)
    py_code = re.sub(r'default:', r'    return', py_code)
    py_code = re.sub(r'JSON\.stringify\((.*?)\)', r'str(\1)', py_code)
    py_code = re.sub(r'JSON\.parse\((.*?)\)', r'eval(\1)', py_code)
    py_code = re.sub(r'(\w+)\.map\((.*?)\)', r'[\1 for item in \2]', py_code)
    py_code = re.sub(r'(\w+)\.filter\((.*?)\)', r'[\1 for item in \2 if ', py_code)
    py_code = re.sub(r'(\w+)\.reduce\((.*?)\)', r'reduce(lambda x, y: ', py_code)
    py_code = re.sub(r'\n\s*\n', '\n', py_code).strip()

    return py_code

def write_py_file(file_path, py_code):
    with open(file_path, 'w') as file:
        file.write(py_code)
if __name__ == "__main__":
    js_code = read_js_file('example.js')
    py_code = translate_js_to_py(js_code)
    write_py_file('translated.py', py_code)