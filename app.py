from flask import Flask, jsonify, request
from flask_socketio import SocketIO
from sdk_interaction import NIC500SDK
import threading

app = Flask(__name__)
socketio = SocketIO(app)
sdk = NIC500SDK('192.168.20.221')


@app.route('/initialize', methods=['GET'])
def initialize():
    if sdk.initialize_system():
        return jsonify({"message": "Initialized successfully"}), 200
    else:
        return jsonify({"message": "Initialization failed"}), 500


@app.route('/power_on', methods=['POST'])
def power_on():
    response = sdk.power_on_gpr()
    if response:
        return jsonify(response), 200
    else:
        return jsonify({"message": "Failed to power on"}), 500


@app.route('/system_info', methods=['GET'])
def system_info():
    response = sdk.get_system_info()
    if response:
        return jsonify(response), 200
    else:
        return jsonify({"message": "Failed to retrieve system information"}), 500


@app.route('/gpr_system_info', methods=['GET'])
def gpr_system_info():
    response = sdk.get_gpr_system_info()
    if response:
        return jsonify(response), 200
    else:
        return jsonify({"message": "Failed to retrieve GPR system information"}), 500


@app.route('/start_acquisition', methods=['POST'])
def start_acquisition():
    response = sdk.start_acquisition()
    if response:
        return jsonify(response), 200
    else:
        return jsonify({"message": "Failed to start acquisition"}), 500


@app.route('/stop_acquisition', methods=['POST'])
def stop_acquisition():
    response = sdk.stop_acquisition()
    if response:
        return jsonify(response), 200
    else:
        return jsonify({"message": "Failed to stop acquisition"}), 500


@socketio.on('connect')
def handle_connect():
    print('Client connected')


@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')


def send_real_time_data():
    data_socket_info = sdk.get_data_socket()
    if not data_socket_info:
        return
    data_socket_port = data_socket_info['data']['data_socket']['port']

    while True:
        traces = sdk.fetch_trace_data(data_socket_port)
        for trace in traces:
            socketio.emit('data', trace)
        socketio.sleep(1)  # Adjust sleep time as necessary


if __name__ == '__main__':
    threading.Thread(target=send_real_time_data).start()
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
