from flask import Flask, request, jsonify
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

app = Flask(__name__)

# Khóa cho lớp mã hóa đầu tiên (Fernet)
key1 = Fernet.generate_key()
cipher_suite1 = Fernet(key1)

# Khóa và IV cho lớp mã hóa thứ hai (AES)
key2 = os.urandom(32)  # 256-bit key cho AES
iv = os.urandom(32)    # 128-bit IV cho chế độ CBC của AES

def aes_encrypt(data, key, iv):
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    # Dữ liệu cần có độ dài bội số của 16 cho AES-CBC, do đó cần padding
    padded_data = data + b" " * (16 - len(data) % 16)  # Thêm padding đơn giản
    return encryptor.update(padded_data) + encryptor.finalize()

def aes_decrypt(data, key, iv):
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(data) + decryptor.finalize()
    return decrypted_data.rstrip(b" ")  # Bỏ padding

@app.route('/encode_salary', methods=['POST'])
def encode_salary():
    try:
        data = request.get_json()
        salary = str(data.get('salary')).encode('utf-8')
        
        # Lớp mã hóa đầu tiên (Fernet)
        encoded_salary = cipher_suite1.encrypt(salary)
        
        # Lớp mã hóa thứ hai (AES)
        double_encoded_salary = aes_encrypt(encoded_salary, key2, iv)
        
        return jsonify({
            'encoded_salary': double_encoded_salary.hex(),  # Chuyển sang dạng hex để dễ truyền tải
            'iv': iv.hex(),  # Truyền IV để giải mã lại
            'message': 'Mã hóa hai lớp (Fernet + AES) thành công'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/decode_salary', methods=['POST'])
def decode_salary():
    try:
        data = request.get_json()
        double_encoded_salary = bytes.fromhex(data.get('encoded_salary'))  # Chuyển từ hex về bytes
        iv_received = bytes.fromhex(data.get('iv'))  # Lấy lại IV từ yêu cầu
        
        # Giải mã lớp AES
        encoded_salary = aes_decrypt(double_encoded_salary, key2, iv_received)
        
        # Giải mã lớp Fernet
        decoded_salary = cipher_suite1.decrypt(encoded_salary).decode('utf-8')
        
        return jsonify({
            'decoded_salary': decoded_salary,
            'message': 'Giải mã hai lớp (AES + Fernet) thành công'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
