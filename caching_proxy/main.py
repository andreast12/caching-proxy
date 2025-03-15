import click
from .server import start_server, clear_cache

@click.command()
@click.version_option("0.1.0", prog_name="caching-proxy")
@click.option("--port", type=int, help="Port to run the server on")
@click.option("--origin", help="Origin server to proxy requests to")
@click.option("--clear-cache", "clear_cache_flag", is_flag=True, help="Clear the cache")
def cli(port, origin, clear_cache_flag):
    """Start a caching proxy server"""

    if not clear_cache_flag and (port is None or origin is None):
        raise click.UsageError("You must provide both --port and --origin, or use --clear-cache.")
    elif clear_cache_flag and (port is not None or origin is not None):
        raise click.UsageError("You cannot use --clear-cache with --port or --origin.")

    if clear_cache_flag:
        clear_cache()
    else:
        start_server(origin, port)

if __name__ == "__main__":
    cli()