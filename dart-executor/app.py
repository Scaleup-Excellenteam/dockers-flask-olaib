import os
import subprocess
import tempfile
from flask import Flask, request, jsonify

app = Flask(__name__)

ERROR_INVALID_CODE = {'error': 'Invalid code'}
ERROR_NO_CODE_PROVIDED = {'error': 'No code provided'}
DART_COMMAND = ['dart']
BAD_REQUEST = 400


@app.errorhandler(Exception)
def handle_error(e):
    return jsonify({'error': str(e)}), 500


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
        output = execute_dart_code(code)
        return jsonify({'output': output})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def execute_dart_code(code):
    # Create a temporary Dart file
    with tempfile.NamedTemporaryFile(suffix='.dart', delete=False) as tmp_file:
        tmp_file.write(code.encode('utf-8'))
        tmp_file.flush()
    try:
        # Compile and execute the Dart code
        result = subprocess.run(DART_COMMAND + [tmp_file.name],
                                capture_output=True,
                                text=True)
        output = result.stdout
        if result.returncode != 0:
            raise Exception(result.stderr)
        return output
    finally:
        # Clean up the temporary file
        os.unlink(tmp_file.name)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
