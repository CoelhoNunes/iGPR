# GPR-ARC: Advanced Radar Control for Geophysical Exploration

Welcome to **GPR-ARC**, the pinnacle of innovation in Ground Penetrating Radar (GPR) data acquisition and analysis, meticulously crafted as part of my PhD work in Electrical and Computer Engineering. GPR-ARC embodies a novel approach to controlling GPR devices, processing data, and employing advanced computational techniques, including artificial intelligence and machine learning, to unveil the secrets hidden beneath the surface.

```

███████╗██╗██╗   ██╗               █████╗ ██████╗  ██████╗
██╔════╝██║██║   ██║              ██╔══██╗██╔══██╗██╔════╝
█████╗  ██║██║   ██║    █████╗    ███████║██████╔╝██║     
██╔══╝  ██║██║   ██║    ╚════╝    ██╔══██║██╔══██╗██║     
██║     ██║╚██████╔╝              ██║  ██║██║  ██║╚██████╗
╚═╝     ╚═╝ ╚═════╝               ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝
                                                          

```

## Core Features

- **Programmatic GPR Control**: Directly manipulate GPR settings and initiate scans with our intuitive Python API.
- **Live Data Streaming**: Capture real-time GPR data for immediate processing and visualization.
- **Sophisticated Signal Processing**: Employ advanced algorithms for signal cleaning, enhancement, and analysis.
- **AI and Machine Learning**: Utilize cutting-edge AI for feature extraction, classification, and predictive modeling, integrating seamlessly with TensorFlow and PyTorch.
- **Dynamic Visualization**: Explore your GPR data through our interactive visualization suite, supporting both 2D and 3D data representations.
- **Modular Design**: Crafted for flexibility, allowing for easy integration of additional tools and libraries to suit various research needs.

## What's Next?

- **Deep Learning for Subsurface Analysis**: Implement deep neural networks to identify and classify subsurface features with unprecedented accuracy automatically.
- **Virtual Reality (VR) Integration**: Step into your data with VR support, offering an immersive way to analyze and interpret GPR findings.
- **Automated Survey Path Planning**: Integrate automated path planning for unmanned aerial vehicles (UAVs) and robotic systems, optimizing data collection.
- **Collaborative Platform**: A web-based platform for sharing, annotating, and discussing GPR datasets within the research community.

## Getting Started

To embark on your journey with GPR-ARC:

1. **Clone and Setup**

   ```sh
   git clone https://github.com/YourUsername/GPR-ARC.git
   cd GPR-ARC
   pip install -r requirements.txt
   ```

2. **Run**

   Begin by setting up your GPR device's IP in the configuration file. Execute the main script to launch the data acquisition process:

   ```sh
   python gpr_arc.py
   ```

## Troubleshooting Guide

### Environment Setup Issues

1. **Python Not Installed or Outdated**: Make sure Python 3.6 or newer is installed. Use `python --version` to check your current version. If it still needs to be installed or updated, download the latest version from the official Python website.

2. **Missing Libraries**: If you encounter errors related to missing `requests` or `numpy` libraries, ensure they are installed by running `pip install requests numpy`. If `pip` is not recognized, verify that Python and Pip are correctly installed and added to your system's PATH.

3. **Network Configuration**: Verify the NIC500 device is properly connected to your network. If the device is not communicating, check your network cables and router settings and ensure the device's IP address is correctly configured. Adjust the script's `IP_ADDRESS` variable if your device uses a different IP.

4. **NIC500 Not in SDK Mode**: If the script cannot communicate with the NIC500, ensure the device is in SDK mode. Consult the NIC500's user manual for instructions on enabling SDK mode, as this step is crucial for programmatic control.

5. **Network Resources**: Since the script is making network requests to a specific IP address and port, ensure that the target device (NIC with IP ADRESS) is reachable and the specified ports are open. The error might be misleading if it's thrown by the socket.connect method, which might fail if the IP address or port is incorrect, or the device is not reachable in your network.

6.**SSL/TLS Certificates**: Your script uses HTTPS ("https://{IP_ADDRESS}:8080/api") for requests. If your NIC device uses a self-signed certificate or a certificate not recognized by Python's requests library, it could lead to issues not typically indicated by [Errno 2]. You might need to either add the certificate to your trusted certificates or modify the script to ignore SSL certificate verification (not recommended for production environments). 

  **Check Network Accessibility: Use tools like ping or telnet to ensure the NIC device is reachable**
  ```sh
  ping 192.000.00.000
  telnet 192.000.00.000 8080
   ```
  **SSL/TLS Certificate Verification**: Temporarily disable SSL certificate verification as a troubleshooting step (remember, this is not secure and should only be used for debugging purposes). Modify your send_request function:
  ```sh
  response = requests.get(url, verify=False)  # For GET
  response = requests.put(url, json=data, verify=False)  # For PUT
   ```

**Note**: If disabling SSL verification resolves your issue, consider properly handling SSL certificates, such as adding your device's certificate to the trusted store, or configuring your script to use a custom CA bundle for verification.
 
**Socket Connection**: If the error arises from the socket.connect line, verify that the device is configured to accept connections on the specified port. If you're not sure, consult the device's documentation or your network administrator to ensure the port is correctly configured and not blocked by a firewall.


### Running the Script Issues

1. **Script Fails to Open**: Ensure your text editor or IDE is correctly installed and functioning. If you cannot open the script, check for any software updates or try reinstalling the editor.

2. **Incorrect IP Address or Parameters**: Double-check the `IP_ADDRESS` and `GPR_CONFIG` in the script. Incorrect settings can lead to communication failures or incorrect data acquisition setups. Ensure these settings match your specific hardware and research needs.

3. **Script Not Executing**: If the script doesn't run or stops with an error, make sure you're in the correct directory in your terminal or command prompt. Use `cd path/to/script` to navigate to the script's folder. Check for syntax errors or missing dependencies in the error messages provided.

4. **No Output or Error Messages**: If the script runs but doesn't produce any output or displays error messages, verify your device's connectivity and ensure it's powered on. Check the console or log messages for clues on what might be wrong.

### Data Acquisition and Extraction Issues

1. **Data Acquisition Not Starting**: Ensure the data acquisition command is correctly implemented in the script and that the GPR device is ready for data collection. Check the device's status lights or interface to confirm it's in the correct mode for data acquisition.

2. **Not Receiving Data**: If data is not being received as expected, verify the data socket connection details, including the port number and IP address. Ensure your firewall or network settings are not blocking the connection. Test the socket connection separately using a network tool or a simple socket test script.

By following these troubleshooting steps, you should be able to identify and resolve common issues encountered when configuring and operating the GPR through the NIC. Remember, careful setup and attention to detail are key to successful data acquisition and analysis with GPR-ARC.


## Contributing

As part of my PhD journey, GPR-ARC is a testament to the power of open collaboration. Your contributions, whether they be new features, improvements, or bug reports, are invaluable. Please feel free to reach out, submit an issue, or pull a request.

## Support and Community

Join our burgeoning community for discussions, support, and insights into GPR-ARC. Detailed documentation and a user forum are available to assist you in your exploration endeavors.

---

**Embark on a voyage of discovery with GPR-ARC, where engineering innovation meets the mysteries of the subsurface.**
