from flask import Flask, request, jsonify
from cryptography.fernet import Fernet

app = Flask(__name__)

# Tạo hai khóa mã hóa
key1 = Fernet.generate_key()
key2 = Fernet.generate_key()

cipher_suite1 = Fernet(key1)
cipher_suite2 = Fernet(key2)

@app.route('/encode_salary', methods=['POST'])
def encode_salary():
    try:
        data = request.get_json()
        salary = str(data.get('salary')).encode('utf-8')
        
        # Lớp mã hóa đầu tiên
        encoded_salary = cipher_suite1.encrypt(salary)
        # Lớp mã hóa thứ hai
        double_encoded_salary = cipher_suite2.encrypt(encoded_salary)
        
        return jsonify({
            'encoded_salary': double_encoded_salary.decode('utf-8'),
            'message': 'Mã hóa hai lớp thành công'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/decode_salary', methods=['POST'])
def decode_salary():
    try:
        data = request.get_json()
        double_encoded_salary = data.get('encoded_salary').encode('utf-8')
        
        # Giải mã lớp thứ hai
        encoded_salary = cipher_suite2.decrypt(double_encoded_salary)
        # Giải mã lớp thứ nhất
        decoded_salary = cipher_suite1.decrypt(encoded_salary).decode('utf-8')
        
        return jsonify({
            'decoded_salary': decoded_salary,
            'message': 'Giải mã hai lớp thành công'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
