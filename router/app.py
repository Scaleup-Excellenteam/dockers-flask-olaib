import os

from flask import Flask, request, jsonify
import requests
from config import MESSAGES, EXECUTOR_URLS, EXECUTOR_EXTENSIONS, app, \
    CODES_DIR_NAME, FILE, EXTENSION_SEPARATOR


@app.errorhandler(Exception)
def handle_error(e):
    return jsonify({'error': str(e)}), 500


def get_file_extension(filename: str) -> str:
    return filename.split(EXTENSION_SEPARATOR)[-1]


def check_file_extension(filename: str) -> bool:
    file_extension = get_file_extension(filename)
    return file_extension in EXECUTOR_URLS.keys()


def create_dir(dir_name: str) -> None:
    os.makedirs(dir_name, exist_ok=True)


def save_file_in_dir(file, dir_name: str) -> None:
    create_dir(dir_name)
    file.save(os.path.join(dir_name, file.filename))


@app.route('/code', methods=['POST'])
def receive_code():
    if FILE not in request.files:
        return jsonify({'error': MESSAGES['FILE_MISSING']}), 400

    file = request.files[FILE]

    if file.filename == '':
        return jsonify({'error': MESSAGES['UNSELECTED_FILE']}), 400
    if not check_file_extension(file.filename):
        return jsonify({'error': f"{MESSAGES['FILE_NOT_SUPPORTED']}, \
        supported extensions are: {', .'.join(EXECUTOR_URLS.keys())}"}), 400

    save_file_in_dir(file, CODES_DIR_NAME)

    return jsonify({'message': MESSAGES['FILE-RECEIVED']})


@handle_error
@app.route('/execute', methods=['GET'])
def execute_code():
    if os.path.exists(CODES_DIR_NAME):
        create_dir(CODES_DIR_NAME)

    code_files = [os.path.join(CODES_DIR_NAME, filename) for filename in os.listdir(CODES_DIR_NAME) if
                  os.path.isfile(os.path.join(CODES_DIR_NAME, filename)) \
                  and filename.split(EXTENSION_SEPARATOR)[-1] in EXECUTOR_EXTENSIONS]

    if len(code_files) == 0:
        return jsonify({'message': MESSAGES['NO_CODE_FILES']}), 400

    results = {}

    for code_file in code_files:
        extension = get_file_extension(code_file)
        executor_url = get_executor_url(extension)

        if executor_url:
            try:
                code = open(code_file, 'r').read()
                response = requests.post(executor_url, json={'code': code})
                response.raise_for_status()
                results[code_file] = response.json()
            except requests.exceptions.RequestException as e:
                results[code_file] = {'error': str(e)}

    return jsonify(results)


def get_executor_url(extension: str) -> str:
    if extension in EXECUTOR_URLS:
        return EXECUTOR_URLS[extension]
    else:
        raise Exception(f'No executor found for {extension} extension')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
