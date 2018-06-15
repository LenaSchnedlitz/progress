import io
import logging

from flask import Flask, abort, render_template, request, send_file

from format import Format

app = Flask(__name__)


def file(dividend, divisor, theme):
    """Return a progress bar .svg-file for the given parameters"""

    try:
        svg = Format.create(dividend, divisor, theme).svg()
        buffer = io.BytesIO()
        buffer.write(svg.encode())
        buffer.seek(0)
        return send_file(buffer, mimetype='image/svg+xml')
    except ValueError:
        logging.error("SVG creation failed.")
        abort(404)


@app.errorhandler(404)
def file_not_found(_):
    return render_template('error.html'), 404


@app.route("/")
def home():
    return render_template('main.html')


@app.route("/<int:dividend>")
@app.route("/<int:dividend>/<int:divisor>")
@app.route("/<int:dividend>/<int:divisor>/<theme>")
def load(dividend, divisor=100, theme='default'):
    return file(dividend, divisor, theme)


@app.route("/", methods=['POST'])
def redirect():
    dividend = int(request.form['dividend'])
    divisor = int(request.form['divisor'])

    theme = request.form['theme']
    if theme == "Custom Color":
        theme = request.form['color'][1:]

    return file(dividend, divisor, theme)


if __name__ == '__main__':
    app.run()
