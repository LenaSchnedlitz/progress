from flask import Flask, render_template, send_file

import io

import format

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('main.html')


@app.route('/<int:dividend>')
@app.route('/<int:dividend>/<int:divisor>')
@app.route('/<int:dividend>/<int:divisor>/<palette>')
def load(dividend, divisor=100, palette='TRAFFIC_LIGHT'):
    percent = format.percentage(dividend, divisor)

    with open('static/svg/progress.svg') as svg_file:
        svg = svg_file.read()
        buffer = io.BytesIO()
        buffer.write(svg.format(percent).encode())
        buffer.seek(0)
        return send_file(buffer, mimetype='image/svg+xml')


if __name__ == '__main__':
    app.run()
