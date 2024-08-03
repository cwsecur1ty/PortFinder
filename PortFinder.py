import argparse
import asyncio
import socket
import logging
from aiofiles import open as aio_open

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to resolve a URL to an IP address
async def resolve_host(host):
    try:
        loop = asyncio.get_event_loop()
        ip_address = await loop.run_in_executor(None, socket.gethostbyname, host)
        return ip_address
    except Exception as e:
        logging.error(f"Error resolving host {host}: {e}")
        return None

# Function to scan a single port asynchronously
async def scan_port(host, port):
    try:
        reader, writer = await asyncio.wait_for(asyncio.open_connection(host, port), timeout=1)
        writer.close()
        await writer.wait_closed()
        return port
    except asyncio.TimeoutError:
        return None
    except Exception as e:
        logging.error(f"Error scanning port {port} on {host}: {e}")
        return None

# Function to scan a range of ports asynchronously
async def scan_ports(host, start_port, end_port):
    tasks = [scan_port(host, port) for port in range(start_port, end_port + 1)]
    open_ports = await asyncio.gather(*tasks)
    return [port for port in open_ports if port is not None]

# Function to save results to a file
async def save_results(filename, host, open_ports):
    async with aio_open(filename, 'w') as file:
        await file.write(f"Open ports on {host}:\n")
        for port in open_ports:
            await file.write(f"{port}\n")

# Main function to parse arguments and initiate scanning
async def main():
    parser = argparse.ArgumentParser(description="Advanced Port Scanner")
    parser.add_argument("-H", "--hosts", required=True, help="Comma-separated list of target IP addresses or URLs")
    parser.add_argument("-s", "--start-port", type=int, default=1, help="Starting port number")
    parser.add_argument("-e", "--end-port", type=int, default=65535, help="Ending port number")
    parser.add_argument("-o", "--output", help="File to save results")
    parser.add_argument("--timeout", type=int, default=1, help="Timeout for connections in seconds")

    args = parser.parse_args()

    hosts = [host.strip() for host in args.hosts.split(',')]
    start_port = args.start_port
    end_port = args.end_port
    output_file = args.output

    for host in hosts:
        logging.info(f"Scanning {host} from port {start_port} to {end_port}...")
        resolved_host = await resolve_host(host)
        if resolved_host:
            open_ports = await scan_ports(resolved_host, start_port, end_port)
            logging.info(f"Scanning completed. Open ports: {open_ports}")
            if output_file:
                await save_results(output_file, resolved_host, open_ports)
        else:
            logging.error("Scanning failed due to unresolved host.")

if __name__ == "__main__":
    asyncio.run(main())
