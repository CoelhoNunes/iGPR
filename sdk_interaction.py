import json
import requests
import socket
import struct
import numpy as np


class NIC500SDK:
    def __init__(self, ip_address):
        self.ip_address = ip_address
        self.api_url = f"http://{self.ip_address}:8080/api"
        self.commands = {
            "system_info": f"{self.api_url}/nic/system_information",
            "gpr_system_info": f"{self.api_url}/nic/gpr/system_information",
            "data_socket": f"{self.api_url}/nic/gpr/data_socket",
            "version": f"{self.api_url}/nic/version",
            "power": f"{self.api_url}/nic/power",
            "setup": f"{self.api_url}/nic/setup",
            "acquisition": f"{self.api_url}/nic/acquisition"
        }
        self.settings = {
            "points_per_trace": 200,
            "time_sampling_interval_ps": 100,
            "point_stacks": 4,
            "period_s": 1,
            "first_break_point": 20,
            "header_size_bytes": 20,
            "point_size_bytes": 4
        }
        self.power_on_config = {"data": json.dumps({'state': 2})}
        self.start_acquisition_config = {"data": json.dumps({'state': 1})}
        self.stop_acquisition_config = {"data": json.dumps({'state': 0})}

    def get_request(self, command):
        try:
            response = requests.get(command)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error during GET request to {command}: {e}")
            return None

    def put_request(self, command, data):
        try:
            response = requests.put(command, data=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error during PUT request to {command}: {e}")
            return None

    def initialize_system(self):
        api_response = self.get_request(self.api_url)
        if api_response is None or api_response.get('data', {}).get('name') != "NIC-500 SDK":
            print("Not in NIC SDK Mode")
            return False
        print("In NIC SDK Mode!")
        return True

    def power_on_gpr(self):
        return self.put_request(self.commands['power'], self.power_on_config)

    def get_system_info(self):
        return self.get_request(self.commands['system_info'])

    def get_gpr_system_info(self):
        return self.get_request(self.commands['gpr_system_info'])

    def get_data_socket(self):
        return self.get_request(self.commands['data_socket'])

    def setup_gpr(self, window_time_shift_ps):
        setup_nic_configuration = {
            'data': json.dumps({
                "gpr0": {"parameters": {
                    'points_per_trace': self.settings['points_per_trace'],
                    'window_time_shift_ps': window_time_shift_ps,
                    'point_stacks': self.settings['point_stacks'],
                    'time_sampling_interval_ps': self.settings['time_sampling_interval_ps']
                }},
                "timer": {"parameters": {"period_s": self.settings['period_s']}}
            })
        }
        return self.put_request(self.commands['setup'], setup_nic_configuration)

    def start_acquisition(self):
        return self.put_request(self.commands['acquisition'], self.start_acquisition_config)

    def stop_acquisition(self):
        return self.put_request(self.commands['acquisition'], self.stop_acquisition_config)

    def fetch_trace_data(self, data_socket_port):
        data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        data_socket.connect((self.ip_address, data_socket_port))
        gpr_data = b''
        gpr_data_size_bytes = self.settings['header_size_bytes'] + (
                self.settings['points_per_trace'] * self.settings['point_size_bytes'])
        trace_num = 0

        traces = []

        while trace_num < 10:
            gpr_data += data_socket.recv(gpr_data_size_bytes)
            num_traces_received = int(len(gpr_data) / gpr_data_size_bytes)

            for i in range(num_traces_received):
                header = struct.unpack('<LLLLHH', gpr_data[:self.settings['header_size_bytes']])
                s = gpr_data[self.settings['header_size_bytes']:gpr_data_size_bytes]
                gpr_data = gpr_data[gpr_data_size_bytes:]
                trace_num = header[2]
                trace_points = np.frombuffer(s, dtype=np.float32).tolist()
                traces.append({
                    "header": header,
                    "points": trace_points
                })

        data_socket.close()
        return traces
