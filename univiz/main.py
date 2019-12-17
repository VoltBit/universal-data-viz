from flask import Flask, render_template, send_from_directory

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/ddmetrics')
def ddmetrics():
    print("Hello")
    return render_template('result.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=80)
