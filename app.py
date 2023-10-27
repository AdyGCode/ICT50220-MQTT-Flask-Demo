from flask import Flask, render_template, request, jsonify
from flask_mqtt import Mqtt
app = Flask(__name__)

app.config['MQTT_BROKER_URL'] = 'l306-25.local'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = ''  # Set this item when you need to verify username and password
app.config['MQTT_PASSWORD'] = ''  # Set this item when you need to verify username and password
app.config['MQTT_KEEPALIVE'] = 5  # Set KeepAlive time in seconds
app.config['MQTT_TLS_ENABLED'] = False  # If your server supports TLS, set it True
topic = '/flask/mqtt'

mqtt_client = Mqtt(app)

@mqtt_client.on_connect()
def handle_connect(client, userdata, flags, rc):
   if rc == 0:
       print('Connected successfully')
       mqtt_client.subscribe(topic) # subscribe topic
   else:
       print('Bad connection. Code:', rc)


@mqtt_client.on_message()
def handle_mqtt_message(client, userdata, message):
   data = dict(
       topic=message.topic,
       payload=message.payload.decode()
  )
   print('Received message on topic: {topic} with payload: {payload}'.format(**data))

@app.route('/publish', methods=['POST'])
def publish_message():
   request_data = request.get_json()
   publish_result = mqtt_client.publish(request_data['topic'], request_data['msg'])
   return jsonify({'code': publish_result[0]})

@app.route('/test')
def test():
    return render_template('test.html')


@app.route('/passing')
@app.route('/passing/<name>')
def passing(name="frank"):
    name = name.capitalize()
    return render_template('passing.html', given_name=name)


@app.route('/test-fail')
def test_fail():
    return render_template('index-fail.html')


@app.route('/pycharm')
def pycharm():
    return render_template('pycharm.html')

@app.route('/')
def index():  # put application's code here
    # return 'Hello World!'
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
