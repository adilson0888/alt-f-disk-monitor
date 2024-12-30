import os
import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify
import json

app = Flask(__name__)

class StorageDevice:
    def __init__(self, device, label, capacity, available, fs, mode, dirty, fsck):
        self.device = device
        self.label = label
        self.capacity = capacity
        self.available = available
        self.fs = fs
        self.mode = mode
        self.dirty = dirty
        self.fsck = fsck

    def __str__(self):
        return (f"Device: {self.device}\n"
                f"Label: {self.label}\n"
                f"Capacity: {self.capacity}\n"
                f"Available: {self.available}\n"
                f"File System: {self.fs}\n"
                f"Mode: {self.mode}\n"
                f"Dirty: {self.dirty}\n"
                f"FSCK: {self.fsck}")
    def to_dict(self):
        return {
            "device": self.device,
            "label": self.label,
            "capacity": self.capacity,
            "available": self.available,
            "fs": self.fs,
            "mode": self.mode,
            "dirty": self.dirty,
            "fsck": self.fsck
        }
    def to_json(self):
        return json.dumps(self.to_dict(), indent=4)
    
class RaidDevice:
    def __init__(self, device, capacity, level, state, status, action, done, eta):
        self.device = device
        self.capacity = capacity
        self.level = level
        self.state = state
        self.status = status
        self.action = action
        self.done = done
        self.eta = eta

    def __str__(self):
        return (f"Device: {self.device}\n"
                f"Capacity: {self.capacity}\n"
                f"Level: {self.level}\n"
                f"State: {self.state}\n"
                f"Status: {self.status}\n"
                f"Action: {self.action}\n"
                f"Done: {self.done}\n"
                f"ETA: {self.eta}")

    def to_dict(self):
        return {
            "device": self.device,
            "capacity": self.capacity,
            "level": self.level,
            "state": self.state,
            "status": self.status,
            "action": self.action,
            "done": self.done,
            "eta": self.eta
        }
    def to_json(self):
        return json.dumps(self.to_dict(), indent=4)
    
def get_data():

    # Define the URL of the status page you want to scrape
    url = os.getenv('STATUS_PAGE_URL') + "/cgi-bin/status.cgi"

    # Set the user-agent to avoid being blocked by the website
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    # Send a request to fetch the HTML content of the page
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Check if the request was successful
    soup = BeautifulSoup(response.content, 'html.parser')
    
    return soup

def fetch_device_data():
    
    # Parse the HTML content using Beautiful Soup
    soup = get_data()
    
    table = soup.find("div", id="mounted_filesystems_st").find("table")
    rows = table.find_all('tr')[1:]
    
    devices = []
    for row in rows:
        cols = row.find_all('td')
        device = StorageDevice(
            device=cols[0].text.strip(),
            label=cols[1].text.strip(),
            capacity=cols[2].text.strip(),
            available=cols[3].text.strip(),
            fs=cols[4].text.strip(),
            mode=cols[5].text.strip(),
            dirty=cols[6].text == 'True',
            fsck=cols[7].text.strip()
        )
        
        devices.append(device)

    return devices

def fetch_raid_data():
    
    soup = get_data()
    
    table = soup.find("div", id="raid_st").find("table")
    rows = table.find_all('tr')[1:]
    
    devices = []
    for row in rows:
        cols = row.find_all('td')
        device = RaidDevice(
            device=cols[0].text.strip(),
            capacity=cols[1].text.strip(),
            level=cols[2].text.strip(),
            state=cols[3].text.strip(),
            status=cols[4].text.strip(),
            action=cols[5].text.strip(),
            done=cols[6].text.strip(),
            eta=cols[7].text.strip()
        )
        devices.append(device)

    return devices

@app.route('/devices/<device_name>', methods=['GET'])
def get_device(device_name):
    devices = fetch_device_data()
    for device in devices:
        if device.device == device_name:
            return jsonify(device.to_dict())
    return jsonify({"error": "Device not found"}), 404

@app.route('/raid/<device_name>', methods=['GET'])
def get_raid(device_name):
    devices = fetch_raid_data()
    for device in devices:
        if device.device == device_name:
            return jsonify(device.to_dict())
    return jsonify({"error": "Device not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3800)
