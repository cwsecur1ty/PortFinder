# Python-Port-Scanner

## Description

**Python-Port-Scanner** is a Python-based tool for scanning ports on one or more target IP addresses or URLs. It supports scanning a range of ports, resolving hostnames to IP addresses, and saving scan results to a file. Python-Port-Scanner utilises asynchronous programming to perform efficient and fast scans.

## Features

- **Scan Multiple Hosts**: Scan one or more IP addresses or URLs.
- **Customizable Port Range**: Define the range of ports to scan.
- **Output to File**: Save the results of the scan to a file.
- **Customizable Timeouts**: Adjust connection timeouts.
- **Logging**: Detailed logging for progress and errors.

## Requirements

- Python 3.x or higher
- `aiofiles` library (for saving results to a file)

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/Advanced-Port-Scanner.git
   ```
2. Navigate to the Project Directory
   ```bash
   cd Advanced-Port-Scanner
    ```
3. Install Dependencies
   ```bash
   pip install aiofiles
   ```
## Usage
Python-Port-Scanner can be ran with the following parameters:
```bash
python Python-Port-Scanner.py -H <host1>,<host2> -s <start-port> -e <end-port> [-o <output-file>] [--timeout <timeout>]
```
### Arguments
Arguments
- -H, --hosts (required): Comma-separated list of target IP addresses or URLs.
- -s, --start-port (optional): Starting port number (default is 1).
- -e, --end-port (optional): Ending port number (default is 65535).
- -o, --output (optional): File to save the results.
- --timeout (optional): Timeout for connections in seconds (default is 1).
## Example
To scan ports 1 to 1500 on test.com and save the results to finder.txt:
```bash
python Python-Port-Scanner.py -H test.com -s 1 -e 1000 -o finder.txt
```
To scan mutliple hosts (test.com,test2.com) and save the results to multi-finder.txt.
```bash
python Python-Port-Scanner.py -H example.com,another-example.com -s 1 -e 1000
```
