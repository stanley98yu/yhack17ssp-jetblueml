# @author Stanley Yu
# @date December 2, 2017
# Main program for running JetBlueML web app.
from flask import Flask, render_template, request

app = Flask(__name__)
app.config['DEBUG'] = True


@app.route('/')
def index():
    return render_template('base.html')


@app.route('/submitted', methods=['POST'])
def submitted_form():
    orig = request.form['orig']
    dest = request.form['dest']
    return render_template('submitted.html', orig=orig, dest=dest)


if __name__ == "__main__":
    app.run()
