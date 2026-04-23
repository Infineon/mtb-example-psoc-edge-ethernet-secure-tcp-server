#!/usr/bin/env python

#******************************************************************************
# File Name:   tcp_secure_client.py
#
# Description: A simple python based secure TCP client.
# The server sends LED ON/OFF commands to the connected TCP client
# and receives acknowledgement from the client.
#
#******************************************************************************
# (c) 2019-2026, Infineon Technologies AG, or an affiliate of Infineon
# Technologies AG. All rights reserved.
# This software, associated documentation and materials ("Software") is
# owned by Infineon Technologies AG or one of its affiliates ("Infineon")
# and is protected by and subject to worldwide patent protection, worldwide
# copyright laws, and international treaty provisions. Therefore, you may use
# this Software only as provided in the license agreement accompanying the
# software package from which you obtained this Software. If no license
# agreement applies, then any use, reproduction, modification, translation, or
# compilation of this Software is prohibited without the express written
# permission of Infineon.
# 
# Disclaimer: UNLESS OTHERWISE EXPRESSLY AGREED WITH INFINEON, THIS SOFTWARE
# IS PROVIDED AS-IS, WITH NO WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING, BUT NOT LIMITED TO, ALL WARRANTIES OF NON-INFRINGEMENT OF
# THIRD-PARTY RIGHTS AND IMPLIED WARRANTIES SUCH AS WARRANTIES OF FITNESS FOR A
# SPECIFIC USE/PURPOSE OR MERCHANTABILITY.
# Infineon reserves the right to make changes to the Software without notice.
# You are responsible for properly designing, programming, and testing the
# functionality and safety of your intended application of the Software, as
# well as complying with any legal requirements related to its use. Infineon
# does not guarantee that the Software will be free from intrusion, data theft
# or loss, or other breaches ("Security Breaches"), and Infineon shall have
# no liability arising out of any Security Breaches. Unless otherwise
# explicitly approved by Infineon, the Software may not be used in any
# application where a failure of the Product or any consequences of the use
# thereof can reasonably be expected to result in personal injury.
#******************************************************************************/

#!/usr/bin/env python
import socket
import ssl
import sys

# IP details for the TCP server
DEFAULT_PORT = 50007                         # Port of the TCP server
arguments = len(sys.argv) - 1

if ((arguments == 2) and sys.argv[1] == "ipv4"):
    print("================================================================================")
    print("TCP Secure Client (IPv4 addressing mode)")
    print("================================================================================")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
elif((arguments == 2) and sys.argv[1] == "ipv6"):
    print("================================================================================")
    print("TCP Secure Client (IPv6 addressing mode)")
    print("================================================================================")
    s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
else:
    print("\nInvalid inputs. From the command line, enter IP address type (ipv6 or ipv4) followed by server IP address")
    print("For example:")
    print("If you are using IPv4 addressing mode, enter the command as:")
    print("python tcp_secure_client ipv4 <IPv4 Address>")
    print("If you are using IPv6 addressing mode, enter the command as:")
    print("python tcp_secure_client ipv6 <IPv6 Address>")
    sys.exit(1)

DEFAULT_IP = sys.argv[2]

context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
context.load_cert_chain(certfile="client.crt", keyfile="client.key")
context.load_verify_locations(cafile="root_ca.crt")
ssl_sock = context.wrap_socket(s, server_hostname="myServer")

ssl_sock.connect((DEFAULT_IP, DEFAULT_PORT))
print("Connected to TCP Server (IP Address: ", DEFAULT_IP, "Port: ", DEFAULT_PORT, " )")

try:
    while True:
        print("================================================================================")
        data = ssl_sock.read();
        print("Message from Server:")
        if data.decode('utf-8') == '0':
            print("LED OFF")
            message = 'LED OFF ACK'
            ssl_sock.write(message.encode('utf-8'))
        if data.decode('utf-8') == '1':
            print("LED ON")
            message = 'LED ON ACK'
            ssl_sock.write(message.encode('utf-8'))
        print("Acknowledgement sent to secure TCP server")

except KeyboardInterrupt:
    ssl_sock.close()
    s.close()
    s = None
    print("\nConnection Closed")
    sys.exit(1)

# [] END OF FILE
