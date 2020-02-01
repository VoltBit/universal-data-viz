from flask import Flask, render_template
# from .plotters.datadog_metrics import DDPlotter

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/ddmetrics-max')
def ddmetrics_max():
    return render_template('results_maximum.html')


@app.route('/ddmetrics-avg')
def ddmetrics_avg():
    return render_template('results_average.html')


if __name__ == '__main__':
    # DDPlotter().analyze('../../data/top_avg_metrics_extract_2019-12-17 13_22_15.751858.csv')
    app.run(host='0.0.0.0', debug=True, port=80)
