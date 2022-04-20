from flask import Flask
from flask import request
import json
import index

app = Flask(__name__)


@app.route('/post', methods=['POST'])
def main():
    response = json.dumps(index.handler(request.json, context=None))


if __name__ == '__main__':
    app.run()
