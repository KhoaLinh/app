import random
import time
import ssl

from paho.mqtt import client as mqtt_client


broker = "broker.emqx.io"
port = 8883
topic = "temp/mqtt"
# Generate a Client ID with the publish prefix.
client_id = f"publish-{random.randint(0, 1000)}"
username = "webserver"
password = "47yX37^4"


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.tls_set(
        ca_certs=None,
        certfile=None,
        keyfile=None,
        cert_reqs=ssl.CERT_REQUIRED,
        tls_version=ssl.PROTOCOL_TLS,
        ciphers=None,
    )
    client.connect(broker, port)
    return client

def publish(client):
    msg_count = 1
    while True:
        temperature = round(random.uniform(20, 30), 2)  # Tạo nhiệt độ giả định
        humidity = round(random.uniform(60, 100), 2)  # Tạo độ ẩm giả định
        gas_concentration = round(random.uniform(100, 500), 2)  # Tạo nồng độ khí gas giả định
        msg = f"{temperature},{humidity},{gas_concentration}"
        # Publish message
        result = client.publish(topic, msg)
        if result.rc == mqtt_client.MQTT_ERR_SUCCESS:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        time.sleep(10)  # Đợi 10 giây trước khi gửi dữ liệu tiếp theo


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)
    client.loop_stop()


if __name__ == "__main__":
    run()
