from flask import Flask, jsonify, render_template, request, redirect, url_for
import random
import ssl
from paho.mqtt import client as mqtt_client

app = Flask(__name__)

broker = "broker.emqx.io"
port = 8883
topic = "temp/mqtt"
client_id = f"subscribe-{random.randint(0, 1000)}"
username = "webserver"
password = "47yX37^4"

users = {
    'admin': 'adminpassword',
    'user': 'userpassword'
}

temperature = None
humidity = None
gas_concentration = None  # Khai báo biến global

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
            client.subscribe(topic)
        else:
            print("Failed to connect, return code %d\n", rc)

    def on_message(client, userdata, msg):
        global temperature, humidity, gas_concentration
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        data = msg.payload.decode().split(',')
        temperature, humidity, gas_concentration = float(data[0]), float(data[1]), float(data[2])  # Cập nhật dữ liệu
        

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.on_message = on_message
    client.tls_set(ca_certs=None, certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLS, ciphers=None)
    client.connect(broker, port)
    return client

def get_latest_data():
    # Lấy dữ liệu nhiệt độ và độ ẩm mới nhất từ biến global
    global temperature, humidity, gas_concentration
    return temperature, humidity, gas_concentration

# Trang đăng nhập
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            # Đăng nhập thành công, chuyển hướng đến trang chính
            return redirect(url_for('index', username=request.form['username']))
        else:
            error = 'Invalid Credentials. Please try again.'
    return render_template('login.html', error=error)

# Trang chủ của ứng dụng web
@app.route('/')
def index():
    username = request.args.get('username')
    if username:
        return render_template('index.html', username=username)
    else:
        return redirect(url_for('login'))

# API trả về dữ liệu nhiệt độ và độ ẩm mới nhất
@app.route('/admin/data')
def get_data():
    # Lấy thông tin người dùng từ URL
    username = request.args.get('username')
    
    # Đảm bảo người dùng đã đăng nhập
    if username not in users:
        return jsonify({'error': 'Unauthorized access'}), 401
    else:
        temperature, humidity, gas_concentration = get_latest_data()
        return jsonify({'temperature': temperature, 'humidity': humidity, 'gas_concentration': gas_concentration})


if __name__ == '__main__':
    client = connect_mqtt()
    client.loop_start()
    app.run()
