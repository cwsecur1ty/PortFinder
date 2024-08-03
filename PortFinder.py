import argparse
import asyncio
import socket
import logging
from aiofiles import open as aio_open

# Configure logging to display info and error messages with timestamps
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def resolve_host(host):
    """
    Resolve a hostname or URL to an IP address using an asynchronous method.
    
    Args:
        host (str): The hostname or URL to resolve.
        
    Returns:
        str: The resolved IP address or None if an error occurs.
    """
    try:
        # Use asyncio to perform the blocking socket operation in a non-blocking way
        loop = asyncio.get_event_loop()
        ip_address = await loop.run_in_executor(None, socket.gethostbyname, host)
        return ip_address
    except Exception as e:
        # Log the error if resolution fails
        logging.error(f"Error resolving host {host}: {e}")
        return None

async def scan_port(host, port):
    """
    Scan a single port on a given host to check if it's open.
    
    Args:
        host (str): The target IP address.
        port (int): The port number to check.
        
    Returns:
        int or None: The port number if it's open, None otherwise.
    """
    try:
        # Attempt to open a connection to the specified port
        reader, writer = await asyncio.wait_for(asyncio.open_connection(host, port), timeout=1)
        writer.close()
        await writer.wait_closed()
        # Return the port number if successful
        return port
    except asyncio.TimeoutError:
        # Return None if the connection times out
        return None
    except Exception as e:
        # Log any errors that occur during port scanning
        logging.error(f"Error scanning port {port} on {host}: {e}")
        return None

async def scan_ports(host, start_port, end_port):
    """
    Scan a range of ports on a given host.
    
    Args:
        host (str): The target IP address.
        start_port (int): The starting port number.
        end_port (int): The ending port number.
        
    Returns:
        list: A list of open ports.
    """
    # Create a list of tasks to scan each port asynchronously
    tasks = [scan_port(host, port) for port in range(start_port, end_port + 1)]
    open_ports = await asyncio.gather(*tasks)
    # Filter out the None values and return only the open ports
    return [port for port in open_ports if port is not None]

async def save_results(filename, host, open_ports):
    """
    Save the list of open ports to a file.
    
    Args:
        filename (str): The name of the file to save results.
        host (str): The target IP address.
        open_ports (list): The list of open ports.
    """
    async with aio_open(filename, 'w') as file:
        await file.write(f"Open ports on {host}:\n")
        for port in open_ports:
            await file.write(f"{port}\n")

async def main():
    """
    Parse command-line arguments, resolve hosts, perform port scanning,
    and save results to a file if specified.
    """
    parser = argparse.ArgumentParser(description="Advanced Port Scanner")
    parser.add_argument("-H", "--hosts", required=True, help="Comma-separated list of target IP addresses or URLs")
    parser.add_argument("-s", "--start-port", type=int, default=1, help="Starting port number (default is 1)")
    parser.add_argument("-e", "--end-port", type=int, default=65535, help="Ending port number (default is 65535)")
    parser.add_argument("-o", "--output", help="File to save results")
    parser.add_argument("--timeout", type=int, default=1, help="Timeout for connections in seconds (default is 1)")

    args = parser.parse_args()

    # Split the hosts argument into a list and strip any extra whitespace
    hosts = [host.strip() for host in args.hosts.split(',')]
    start_port = args.start_port
    end_port = args.end_port
    output_file = args.output

    # Scan each host and handle results
    for host in hosts:
        logging.info(f"Scanning {host} from port {start_port} to {end_port}...")
        resolved_host = await resolve_host(host)
        if resolved_host:
            open_ports = await scan_ports(resolved_host, start_port, end_port)
            logging.info(f"Scanning completed. Open ports: {open_ports}")
            if output_file:
                await save_results(output_file, resolved_host, open_ports)
        else:
            logging.error(f"Scanning failed due to unresolved host: {host}")

if __name__ == "__main__":
    asyncio.run(main())
