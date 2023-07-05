import os
import re
import subprocess
import tempfile
from flask import Flask, request, jsonify

app = Flask(__name__)

ERROR_INVALID_CODE = {'error': 'Invalid code'}
ERROR_NO_CODE_PROVIDED = {'error': 'No code provided'}
JAVA_COMMAND = ['java']
BAD_REQUEST = 400


def extract_class_name(code):
    # Extract class name from code
    match = re.search(r'\bclass\s+(\w+)', code)
    if match:
        return match.group(1)
    else:
        raise Exception('Failed to extract class name')


@app.errorhandler(Exception)
def handle_error(e):
    return jsonify(error=str(e)), 500


def validate_code(func):
    def wrapper(*args, **kwargs):
        data = request.get_json()
        if 'code' not in data:
            return jsonify(ERROR_NO_CODE_PROVIDED), BAD_REQUEST

        code = data['code']
        if not isinstance(code, str) or len(code) == 0:
            return jsonify(ERROR_INVALID_CODE), BAD_REQUEST

        return func(*args, **kwargs)

    return wrapper


@app.route('/execute', methods=['POST'])
@validate_code
def execute_code():
    code = request.get_json()['code']
    try:
        output = execute_java_code(code)
        return jsonify({'output': output})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def execute_java_code(code):
    class_name = extract_class_name(code)

    with tempfile.NamedTemporaryFile(suffix='.java', delete=False, prefix=class_name) as temp_file:
        temp_file.write(code.encode('utf-8'))
        temp_file.flush()
        temp_file_name = temp_file.name

        try:
            process = subprocess.run(JAVA_COMMAND + [temp_file_name],
                                     capture_output=True,
                                     text=True)
            output = process.stdout
            if process.returncode != 0:
                raise Exception(process.stderr)

            return output
        finally:
            # Clean up the temporary file
            os.unlink(temp_file_name)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
