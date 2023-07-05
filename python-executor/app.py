from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)


@app.errorhandler(Exception)
def handle_error(e):
    return jsonify({'error': str(e)}), 500


@app.route('/execute', methods=['POST'])
def execute_code():
    data = request.get_json()

    if 'code' not in data:
        return jsonify({'error': 'No code provided'}), 400

    code = data['code']
    if not isinstance(code, str) or len(code) == 0:
        return jsonify({'error': 'Invalid code'}), 400

    try:
        with app.app_context():
            result = execute_python_code(code)
            return jsonify({'output': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def execute_python_code(code):
    process = subprocess.Popen(['python3'],
                               stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               text=True)
    output, error = process.communicate(input=code, timeout=5)
    return output


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
