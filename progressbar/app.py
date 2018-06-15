import io
import logging

from flask import Flask, abort, redirect, render_template, request, \
    send_file, url_for

from format import Format

app = Flask(__name__)


@app.route("/")
def home():
    return render_template('main.html')


@app.route("/<int:dividend>")
@app.route("/<int:dividend>/<int:divisor>")
@app.route("/<int:dividend>/<int:divisor>/<theme>")
def file(dividend, divisor=100, theme='default'):
    try:
        svg = Format.create(dividend, divisor, theme).svg()
        buffer = io.BytesIO()
        buffer.write(svg.encode())
        buffer.seek(0)
        return send_file(buffer, mimetype='image/svg+xml')
    except ValueError:
        logging.error("SVG creation failed.")
        abort(404)


@app.route("/", methods=['POST'])
def redirect_to_file():
    params = request.form.to_dict()

    params['theme'] = params['theme'].lower() \
        if params['theme'] != "Custom Color" \
        else params['color'][1:]

    return redirect("/{dividend}/{divisor}/{theme}".format(**params))


@app.errorhandler(404)
def file_not_found(_):
    return redirect(url_for('error'))


@app.route("/error")
def error():
    return render_template('error.html')


if __name__ == '__main__':
    app.run()
