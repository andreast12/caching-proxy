import click
from server import start_server
import socket
import sys

def is_port_in_use(port, host="127.0.0.1"):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex((host, port)) == 0  # Returns True if port is in use
    
    except OverflowError:
        click.echo("Port number is out of range")
        sys.exit(1)


@click.command()
@click.version_option("0.1.0", prog_name="caching-proxy")
@click.option("--port", required=True, type=int, help="Port to run the server on")
@click.option("--origin", required=True, help="Origin server to proxy requests to")
def cli(port, origin):
    """Start a caching proxy server"""

    click.echo(f"Starting server on port {port} with origin {origin} ...") 
    if is_port_in_use(port):
        click.echo(f"Port {port} is already in use")
        return

    start_server(origin, port)

if __name__ == "__main__":
    cli()