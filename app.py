from flask import Flask, request, jsonify
from cryptography.fernet import Fernet

app = Flask(__name__)

# Tạo một khóa mã hóa duy nhất hoặc lưu vào một file an toàn
key = Fernet.generate_key()
cipher_suite = Fernet(key)

@app.route('/encode_salary', methods=['POST'])
def encode_salary():
    try:
        data = request.get_json()
        salary = str(data.get('salary')).encode('utf-8')
        
        # Mã hóa dữ liệu tiền lương
        encoded_salary = cipher_suite.encrypt(salary)
        
        return jsonify({
            'encoded_salary': encoded_salary.decode('utf-8'),
            'message': 'Mã hóa thành công'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/decode_salary', methods=['POST'])
def decode_salary():
    try:
        data = request.get_json()
        encoded_salary = data.get('encoded_salary').encode('utf-8')
        
        # Giải mã dữ liệu tiền lương
        decoded_salary = cipher_suite.decrypt(encoded_salary).decode('utf-8')
        
        return jsonify({
            'decoded_salary': decoded_salary,
            'message': 'Giải mã thành công'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
