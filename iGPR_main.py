# import requests
# import socket
# import struct
# import numpy as np
#
# # Constants and Endpoints Configuration
# IP_ADDRESS = '192.168.20.221'
# BASE_URL = f"https://{IP_ADDRESS}:8080/api"
# ENDPOINTS = {
#     "version": f"{BASE_URL}/nic/version",
#     "system_info": f"{BASE_URL}/nic/system_information",
#     "gpr_system_info": f"{BASE_URL}/nic/gpr/system_information",
#     "data_socket": f"{BASE_URL}/nic/gpr/data_socket",
#     "power": f"{BASE_URL}/nic/power",
#     "setup": f"{BASE_URL}/nic/setup",
#     "acquisition": f"{BASE_URL}/nic/acquisition"
# }
#
# # GPR Configuration Parameters
# GPR_CONFIG = {
#     "points_per_trace": 200,
#     "time_sampling_interval_ps": 100,
#     "point_stacks": 4,
#     "period_s": 1,
#     "first_break_point": 20
# }
#
#
# def send_request(method, url, data=None):
#     """Generalized request function to handle GET and PUT requests."""
#     try:
#         if method == 'GET':
#             response = requests.get(url)
#         elif method == 'PUT':
#             response = requests.put(url, json=data)
#         else:
#             raise ValueError("Unsupported method type.")
#
#         response.raise_for_status()  # Will raise HTTPError for bad requests
#         return response.json()
#     except requests.RequestException as e:
#         print(f"Request to {url} failed: {e}")
#         return None
#
#
# def setup_gpr():
#     """Main function to set up and acquire data from GPR."""
#     # Step 1: Confirm NIC is in SDK Mode
#     if not send_request('GET', ENDPOINTS['version']):
#         print("NIC is not in SDK Mode or unable to communicate.")
#         return
#
#     # Step 2: Fetch and print system info
#     nic_info = send_request('GET', ENDPOINTS['system_info'])
#     if nic_info:
#         print(f"NIC System Information: {nic_info}")
#
#     # Power on GPR
#     if not send_request('PUT', ENDPOINTS['power'], {"state": 2}):
#         return
#
#     # Fetch GPR system info
#     gpr_info = send_request('GET', ENDPOINTS['gpr_system_info'])
#     if gpr_info:
#         print(f"GPR System Information: {gpr_info}")
#
#     # Connect to GPR Data Socket
#     data_socket_info = send_request('GET', ENDPOINTS['data_socket'])
#     if not data_socket_info:
#         return
#
#     # Establish Socket Connection
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
#         sock.connect((IP_ADDRESS, data_socket_info['data']['port']))
#         # Configure GPR
#         if not send_request('PUT', ENDPOINTS['setup'], GPR_CONFIG):
#             return
#         # Start acquisition
#         if not send_request('PUT', ENDPOINTS['acquisition'], {"state": 1}):
#             return
#
#         # Data acquisition logic here...
#         print("Acquiring data...")
#
#         # Stop acquisition
#         if not send_request('PUT', ENDPOINTS['acquisition'], {"state": 0}):
#             return
#
#
# if __name__ == "__main__":
#     setup_gpr()

import requests
import socket
import struct
import numpy as np
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context
import ssl

# Constants and Endpoints Configuration
IP_ADDRESS = '192.168.20.221'
BASE_URL = f"https://{IP_ADDRESS}:8080/api"
ENDPOINTS = {
    "version": f"{BASE_URL}/nic/version",
    "system_info": f"{BASE_URL}/nic/system_information",
    "gpr_system_info": f"{BASE_URL}/nic/gpr/system_information",
    "data_socket": f"{BASE_URL}/nic/gpr/data_socket",
    "power": f"{BASE_URL}/nic/power",
    "setup": f"{BASE_URL}/nic/setup",
    "acquisition": f"{BASE_URL}/nic/acquisition"
}

# GPR Configuration Parameters
GPR_CONFIG = {
    "points_per_trace": 200,
    "time_sampling_interval_ps": 100,
    "point_stacks": 4,
    "period_s": 1,
    "first_break_point": 20
}


class TLSAdapter(HTTPAdapter):
    '''An adapter for specifying TLS version.'''

    def __init__(self, tls_version=ssl.TLSVersion.TLSv1_2, **kwargs):
        self.tls_version = tls_version
        super().__init__(**kwargs)

    def init_poolmanager(self, *args, **kwargs):
        context = create_urllib3_context()
        context.minimum_version = self.tls_version
        kwargs['ssl_context'] = context
        super().init_poolmanager(*args, **kwargs)


# Create a session and mount the TLSAdapter
session = requests.Session()
session.mount('https://', TLSAdapter())


def send_request(method, url, data=None):
    """Generalized request function to handle GET and PUT requests."""
    try:
        if method == 'GET':
            response = session.get(url)
        elif method == 'PUT':
            response = session.put(url, json=data)
        else:
            raise ValueError("Unsupported method type.")

        response.raise_for_status()  # Will raise HTTPError for bad requests
        return response.json()
    except requests.RequestException as e:
        print(f"Request to {url} failed: {e}")
        return None


def setup_gpr():
    """Main function to set up and acquire data from GPR."""
    # Step 1: Confirm NIC is in SDK Mode
    if not send_request('GET', ENDPOINTS['version']):
        print("NIC is not in SDK Mode or unable to communicate.")
        return

    # Step 2: Fetch and print system info
    nic_info = send_request('GET', ENDPOINTS['system_info'])
    if nic_info:
        print(f"NIC System Information: {nic_info}")

    # Power on GPR
    if not send_request('PUT', ENDPOINTS['power'], {"state": 2}):
        return

    # Fetch GPR system info
    gpr_info = send_request('GET', ENDPOINTS['gpr_system_info'])
    if gpr_info:
        print(f"GPR System Information: {gpr_info}")

    # Connect to GPR Data Socket
    data_socket_info = send_request('GET', ENDPOINTS['data_socket'])
    if not data_socket_info:
        return

    # Establish Socket Connection
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((IP_ADDRESS, data_socket_info['data']['port']))
        # Configure GPR
        if not send_request('PUT', ENDPOINTS['setup'], GPR_CONFIG):
            return
        # Start acquisition
        if not send_request('PUT', ENDPOINTS['acquisition'], {"state": 1}):
            return

        # Data acquisition logic here...
        print("Acquiring data...")

        # Stop acquisition
        if not send_request('PUT', ENDPOINTS['acquisition'], {"state": 0}):
            return


if __name__ == "__main__":
    setup_gpr()
