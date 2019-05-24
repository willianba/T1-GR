# SNMP Manager (T1-GR)
College work for network management class @ PUCRS. It works as an SNMP manager to get info from an agent's MIB.

## Dependencies
In order to run this app it's necessary to have <strong>`TKinter`</strong>, <strong>`easySNMP`</strong>,
<strong>`matplotlib`</strong>, and <strong>`SQlite3`</strong>, all installed with Python 3.7.3 specifically.

To install <strong>`easySNMP`</strong>:
`sudo apt-get install libsnmp-dev snmp-mibs-downloader gcc python-dev` and `pip3 install easysnmp`.

To install <strong>`matplotlib`</strong>:
`pip3 install matplotlib`.

To install <strong>`TKinter`</strong>:
`sudo apt-get install python3-tk tk-dev`.

<strong>`SQlite3`</strong> must be installed by default.
If it doesn't, run: `sudo apt-get install libsqlite3-dev`.

## Executing
To execute the app simply run: `python3 app.py`. It's necessary to have a configured and functional SNMP service.
