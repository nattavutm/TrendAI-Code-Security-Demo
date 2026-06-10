from flask import Flask, request, jsonify
import os

app = Flask(__name__)


@app.route('/health')
def health():
    return jsonify({"status": "ok", "version": "1.0.0"})


@app.route('/api/data')
def get_data():
    # Read AWS region from env (injected via .env file at build time)
    region = os.environ.get('AWS_DEFAULT_REGION', 'unknown')
    return jsonify({"message": "Hello from containerized app!", "region": region})


@app.route('/api/echo')
def echo():
    # TODO: add input validation
    msg = request.args.get('msg', '')
    return jsonify({"echo": msg})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
