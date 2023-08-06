import base64
import os
from io import BytesIO

import click
import numpy as np
import pkg_resources
from bitarray import bitarray
from cryptography.fernet import Fernet
from flask import Flask, jsonify, request, send_file, send_from_directory
from flask_cors import CORS, cross_origin
from PIL import Image


def get_fernet_key(password):
    password_bytes = password.encode('utf-8')
    return base64.urlsafe_b64encode(password_bytes.ljust(32)[:32])

def base64_encode_data(input_str):
    return base64.b64encode(input_str.encode('utf-8'))

def base64_decode_data(encoded_str):
    return base64.b64decode(encoded_str).decode('utf-8')

def text_to_bits(text):
    bits = bitarray()
    bits.frombytes(
        text.encode('utf-8') if isinstance(text, str) 
        else text if isinstance(text, bytes) 
        else TypeError(f"Argument must be str or bytes, not {type(text)}")
    )
    return bits

def bits_to_text(bits):
    return bits.tobytes().decode('utf-8')

def bits_to_bytes(bits):
    return bits.tobytes()

def get_bit_length_as_bytes(length):
    return length.to_bytes(4, byteorder='big')

def get_length_from_bytes(byte_data):
    return int.from_bytes(byte_data, byteorder='big')

def encode_image(image_path, text):
    # Open the image and convert to 8-bit RGBA mode (if it's not already)
    image = Image.open(image_path).convert('RGBA')
    data = np.array(image)

    # Convert text to bits
    bits = text_to_bits(text)

    # Prepend message with its length in bits
    bits = text_to_bits(get_bit_length_as_bytes(len(bits))) + bits

    bit_index = 0
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            for k in range(data.shape[2]):
                # If we have more bits to encode
                if bit_index < len(bits):
                    data[i, j, k] = (data[i, j, k] & 0xFE) | bits[bit_index]
                    bit_index += 1
                else:
                    # No more bits to encode
                    return Image.fromarray(data)

    # If there are still bits left to encode
    if bit_index < len(bits):
        print("Warning: Image not large enough to encode all data. Some data was lost.")
    return Image.fromarray(data)


def decode_image(image):
    data = np.array(image)
    bits = bitarray()

    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            for k in range(data.shape[2]):
                bits.append(data[i, j, k] & 0x1)

    # Get the length of the original message
    original_length = get_length_from_bytes(bits_to_bytes(bits[:32]))
    # Extract the original message using its length
    bits = bits[32:32+original_length]

    return bits_to_text(bits)


app = Flask(__name__, static_folder=pkg_resources.resource_filename('adeso', 'static'))  # noqa: E501

def create_app():
    CORS(app)
    return app

@click.command()
@click.option('--debug', is_flag=True)
def run_app(debug):
    app = create_app()
    app.run(debug=debug)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    # Check if path is a file
    if '.' in path:
        # Serve the file from the static directory
        return send_from_directory(app.static_folder, path)
    else:
        # Path is a directory, serve the corresponding HTML file
        html_file_path = os.path.join(path, 'index.html')
        if os.path.exists(os.path.join(app.static_folder, html_file_path)):
            # The HTML file exists, serve it
            return send_from_directory(app.static_folder, html_file_path)
        else:
            # The HTML file does not exist, serve the main index.html file
            return send_from_directory(app.static_folder, 'index.html')


@app.route('/encryption', methods=['POST'])
@cross_origin()
def encryption():
    data = request.json.get('data')
    password = request.json.get('password')
    action = request.json.get('action').lower()
    
    fernet = Fernet(get_fernet_key(password))
    response_data = 'Action not recognized.'

    if action == 'encrypt':
        response_data = fernet.encrypt(base64_encode_data(data)).decode('utf-8')
    elif action == 'decrypt':
        decrypted_data = fernet.decrypt(data.encode('utf-8'))
        response_data = base64_decode_data(decrypted_data)
        
    return jsonify({'data': response_data})


@app.route('/encoding', methods=['POST'])
@cross_origin()
def encoding():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file'})
    data = request.form.get('data')   
    action = request.form.get('action').lower()
    image = request.files['image']

    if action == 'decode':
        decoded_text = decode_image(Image.open(image))
        return jsonify({'decoded_image': decoded_text})
    elif action == 'encode':
        encoded_image = encode_image(image, data)
        output = BytesIO() #instantiate a BytesIO object
        encoded_image.save(output, format='PNG')
        output.seek(0) #set the position of the stream to the beginning
        return send_file(output, mimetype='image/png', as_attachment=True, download_name='encoded_image.png')  # noqa: E501

if __name__ == "__main__":
    run_app()
