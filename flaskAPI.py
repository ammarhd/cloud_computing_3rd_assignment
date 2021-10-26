from flask import Flask, render_template
import json

app = Flask(__name__)


@app.route('/', methods=['GET'])
def show():
    with open('result.json', "r") as jf:
        j = json.loads(jf.readline())
        dict = list(j.items())

    return render_template("index.html", content=dict)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
