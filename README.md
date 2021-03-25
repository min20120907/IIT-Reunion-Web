# IIT-Reunion-Web

## Summary
A Python Flask based webpage

## Prerequirements

##### Mandatory
- MySQL Server (MariaDB)
- Flask
- Python 3 or later

##### Optional
- Phpmyadmin
- lighttpd

## Installation
Example Environment Ubuntu 20.04LTS
1. Installing Python3, and set it to default:
`sudo apt install mysql-server python3 python-is-python3-y`
2. Import the database "Photos" inside db folder
`mysql -u ${USERNAME} -p ${PASSWORD} Photos < db/Photos.sql`
3. run the flask application
`python index.py`
