from flask import Flask, Response
import requests
import redis
import json
import click

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def start_server(origin, port):
    app = Flask(__name__)

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def proxy(path):
        try:
            target = f"{origin}/{path}"
            cached_response = r.get(target)
            
            if cached_response:
                response = json.loads(cached_response)
                proxied_response = Response(response["content"], response["status"], response["headers"])
                proxied_response.headers["X-Cache"] = "HIT"
                return proxied_response

            else:
                response = requests.get(target)
                proxied_response = Response(response.content, response.status_code)

                # Forward only safe headers
                headers = {key: value for key, value in response.headers.items() if key.lower() not in ['content-encoding', 'content-length', 'transfer-encoding']}
                r.set(target, json.dumps({"content": response.text, "status": response.status_code, "headers": headers}))

                proxied_response.headers = headers
                proxied_response.headers["X-Cache"] = "MISS"
                return proxied_response

        except Exception as e:
            return Response(f"Error: {str(e)}", status=500)

    app.run(port=port, debug=True)

def clear_cache():
    r.flushall()
    click.echo("Cache cleared")