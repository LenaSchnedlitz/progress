import io

from flask import Flask, render_template, send_file

from format import Format

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('main.html')


@app.route('/<int:dividend>')
@app.route('/<int:dividend>/<int:divisor>')
@app.route('/<int:dividend>/<int:divisor>/<palette>')
def load(dividend, divisor=100, palette='TRAFFIC_LIGHT'):
    svg = Format(dividend, divisor, palette).svg()
    buffer = io.BytesIO()
    buffer.write(svg.encode())
    buffer.seek(0)
    return send_file(buffer, mimetype='image/svg+xml')


if __name__ == '__main__':
    app.run()
