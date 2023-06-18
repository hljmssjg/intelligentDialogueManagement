from flask import Flask, Response

app = Flask(__name__)

"""
Run a picture server locally.
Any device connected to the same wifi can open the picture by accessing the server's IP address.
"""
@app.route("/img/<imageId>.png")
def get_frame(imageId):
    with open(r'/home/jiangeng/intelligentDialogueManagement/pythonScript/img/{}.png'.format(imageId), 'rb') as f:
        image = f.read()
        resp = Response(image, mimetype="image/png")
        return resp


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


if __name__ == "__main__":
    app.run(host='172.23.143.156', port=5000)
