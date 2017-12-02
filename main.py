# @author Stanley Yu
# @date December 2, 2017
# Main program for running JetBlueML web app.
from flask import Flask, render_template, request
from jetblue_predict import predictFlights

app = Flask(__name__)
app.config['DEBUG'] = True


@app.route('/')
def index():
    return render_template('base.html')


@app.route('/submitted', methods=['POST'])
def submitted_form():
    orig = int(request.form['orig'])
    lMonth = int(request.form['lMonth'])
    lDay = int(request.form['lMonth'])
    lYear = int(request.form['lMonth'])
    bMonth = int(request.form['bMonth'])
    bDay = int(request.form['bDay'])
    bYear = int(request.form['bYear'])
    flight = predictFlights(orig, lMonth, lDay, lYear, bMonth, bDay, bYear)
    return render_template('submitted.html',
    	orig=orig,
    	lMonth=lMonth,
    	lDay=lDay,
    	lYear=lYear,
    	bMonth=bMonth,
    	bDay=bDay,
    	bYear=bYear)


if __name__ == "__main__":
    app.run()
