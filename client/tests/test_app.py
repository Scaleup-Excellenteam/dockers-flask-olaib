import os
import pytest
from flask import Flask
from flask.testing import FlaskClient
from werkzeug.datastructures import FileStorage

CODES_DIR = "./codes"
CODE_FILENAMES = [filename for filename in os.listdir(CODES_DIR) if os.path.isfile(os.path.join(CODES_DIR, filename))]

# Import your Flask application
from app import app


@pytest.fixture
def client() -> FlaskClient:
    """
    Create a test client for the Flask application.
    """
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def create_temporary_file(extension: str) -> FileStorage:
    """
    Create a temporary file with the specified extension.
    """
    # Replace with your own code to create a temporary file
    # You can use the tempfile module or any other method you prefer
    # Return the file object or FileStorage object
    pass


def test_receive_code_py_extension(client: FlaskClient):
    """
    Test receiving code with a .py file.
    """
    file = create_temporary_file(".py")
    response = client.post("/code", data={"file": file})
    data = response.get_json()
    assert response.status_code == 200
    assert "message" in data


def test_receive_code_dart_extension(client: FlaskClient):
    """
    Test receiving code with a .dart file.
    """
    file = create_temporary_file(".dart")
    response = client.post("/code", data={"file": file})
    data = response.get_json()
    assert response.status_code == 200
    assert "message" in data


def test_receive_code_java_extension(client: FlaskClient):
    """
    Test receiving code with a .java file.
    """
    file = create_temporary_file(".java")
    response = client.post("/code", data={"file": file})
    data = response.get_json()
    assert response.status_code == 200
    assert "message" in data

# Add more test cases to cover different scenarios and functionalities of your router
