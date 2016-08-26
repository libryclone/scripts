#!/usr/bin/env python

import os
import psutil
import requests
import socket
import sys

partitions_to_check = ['/', '/home']
threshold = 80  # alert if disk is fuller than this many percent

slack_url = os.environ.get('SLACK_URL')
if not slack_url:
    sys.stderr.write('Error: SLACK_URL env var not found\n')
    sys.exit(1)

for partition in psutil.disk_partitions():
    if (
            partition.mountpoint in partitions_to_check and
            psutil.disk_usage(partition.mountpoint).percent > threshold
    ):
        payload = {
            'username': 'diskspace',
            'icon_emoji': ':minidisc:',
            'channel': '#tech',
            'text': (
                '<!channel> ' +
                socket.gethostname() + ': disk at ' + partition.mountpoint +
                ' is ' + str(psutil.disk_usage(partition.mountpoint).percent) +
                '% full'
            )
        }
        r = requests.post(slack_url, json=payload)
