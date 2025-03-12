from flask import Flask, Response
import requests
from functools import lru_cache

def start_server(origin, port):
    app = Flask(__name__)

    @lru_cache()
    def make_request(target):
        response = requests.get(target)
        proxied_response = Response(response.content, response.status_code)

        # Forward only safe headers
        for key, value in response.headers.items():
            if key.lower() not in ['content-encoding', 'content-length', 'transfer-encoding']:
                proxied_response.headers[key] = value

        return proxied_response

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def proxy(path):
        try:
            target = f"{origin}/{path}"
            
            cache_before = make_request.cache_info()
            response = make_request(target)
            cache_after = make_request.cache_info()

            if cache_after.hits > cache_before.hits:
                response.headers["X-Cache"] = "HIT"
            else:
                response.headers["X-Cache"] = "MISS"

            return response

        except Exception as e:
            return Response(f"Error: {str(e)}", status=500)

    app.run(port=port)