#!/usr/bin/env python

from django.conf import settings
import binascii

import os
import socket
import ssl
import struct


def send_push(token, payload):
    # Your certificate file
    cert = settings.APN_CERT_LOCATION

    # APNS development server
    apns_address = ('gateway.push.apple.com', 2195)

    # Use a socket to connect to APNS over SSL
    s = socket.socket()
    sock = ssl.wrap_socket(s, ssl_version=ssl.PROTOCOL_SSLv3, certfile=cert)
    sock.connect(apns_address)

    token = token.replace(' ', '')
    # Generate a notification packet
    token = binascii.unhexlify(token)
    fmt = '!cH32sH{0:d}s'.format(len(payload))
    cmd = '\x00'
    message = struct.pack(fmt, cmd, len(token), token, len(payload), payload)
    sock.write(message)
    sock.close()
