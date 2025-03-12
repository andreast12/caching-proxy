from flask import Flask, Response
import requests

def start_server(origin, port):
    app = Flask(__name__)

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def proxy(path):
        try:
            target = f"{origin}/{path}"
            response = requests.get(target)
            proxied_response = Response(response.content, response.status_code)

            # Forward only safe headers
            for key, value in response.headers.items():
                if key.lower() not in ['content-encoding', 'content-length', 'transfer-encoding']:
                    proxied_response.headers[key] = value

            return proxied_response

        except Exception as e:
            return Response(f"Error: {str(e)}", status=500)

    app.run(port=port)