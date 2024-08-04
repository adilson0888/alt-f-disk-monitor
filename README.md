# Disk Health Monitor

This project facilitates the monitoring of the health state of disks using the [alt-f](https://sourceforge.net/projects/alt-f/) project. The standard way to monitor the disks would be using the `netsnmp` package, but I couldn't manage to make it work on my old D-Link DNS-320. So I decided to create this simple page that returns all the disk attributes in JSON format. This allows you to add monitors using tools like [Uptime Kuma](https://github.com/louislam/uptime-kuma), for example.

## Features

- Scrapes disk health data from the alt-f status page
- Exposes disk attributes in JSON format via a simple REST API
- Easy integration with monitoring tools like Uptime Kuma

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/adilson0888/alt-f-disk-monitor
   cd alt-f-disk-monitor
   ```

2. Create a .env file with the URL of your alt-f status page:
  ```env
  STATUS_PAGE_URL=http://nas-ip
  ```

3. Build and start the services using Docker Compose:
  ```bash
  docker-compose up -d
  ```
4. The application will be available at http://localhost:3800.

### Usage
#### API Endpoint
  GET /devices/

  Returns the JSON representation of the specified device.

  **Example:**
  ```bash
  curl http://localhost:3800/devices/sdb3
  ```
  **Response:**
  ```json
  {
    "available": "240.3GB",
    "capacity": "687.1GB",
    "device": "sdb3",
    "dirty": false,
    "fs": "ext4",
    "fsck": "22 mounts or 150 days",
    "label": "",
    "mode": "RW"
  }
  ``` 
## Integration with Uptime Kuma
You can integrate this API with Uptime Kuma to monitor the health state of your disks. Add a new HTTP monitor in Uptime Kuma using the Http(s) - Json Query
So you can set expected values to any of the disk attributes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments
[alt-f](https://sourceforge.net/projects/alt-f/)
[Uptime Kuma](https://github.com/louislam/uptime-kuma)

  

