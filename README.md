# Caching Proxy

A lightweight HTTP caching proxy service that sits between your application and external APIs. It caches responses from origin servers to reduce latency and external API calls.

## Requirements

- One of the recent Python releases
- Redis server running on localhost:6379

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/caching-proxy.git
cd caching-proxy
```

### 2. Create and activate a virtual environment

#### On Windows:

```bash
python -m venv env
env\Scripts\activate
```

#### On macOS/Linux:

```bash
python -m venv env
source env/bin/activate
```

### 3. Install the package in development mode

```bash
pip install -e .
```

This will install all required dependencies and make the `caching-proxy` command available in your environment.

## Usage

### Starting the proxy server

```bash
caching-proxy --port <port_number> --origin <origin_url>
```

For example:

```bash
caching-proxy --port 8000 --origin https://api.example.com
```

This will start the proxy server on port 8000, forwarding requests to https://api.example.com and caching the responses.

### Clearing the cache

To clear all cached responses:

```bash
caching-proxy --clear-cache
```

### Getting help

For a complete list of available options:

```bash
caching-proxy --help
```
