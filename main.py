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
    flightName = ['JFK', 'ACK', 'OAK', 'BWI', 'BTV', 'ANU', 'POS', 'LAX', 
    'PHX', 'PSP', 'SEA', 'STI', 'GND', 'ALB', 'HOG', 'PLS', 'ABQ', 'SAV', 
    'DTW', 'SMF', 'CUR', 'CUN', 'TPA', 'LGB', 'HPN', 'UIO', 'SRQ', 'BDL', 
    'GCM', 'SXM', 'BUR', 'SNU', 'IAD', 'STX', 'DCA', 'BGI', 'PBI', 'BUF', 
    'SJO', 'MEX', 'PAP', 'PSE', 'MBJ', 'ORD', 'CLT', 'MSY', 'SFO', 'PIT', 
    'BOG', 'SJU', 'DAB', 'AUS', 'HOU', 'MVY', 'DFW', 'BDA', 'PHL', 'BQN', 
    'LAS', 'RDU', 'PWM', 'FLL', 'MCO', 'UVF', 'DEN', 'CTG', 'HAV', 'RNO', 
    'SJC', 'RIC', 'LGA', 'ORH', 'CHS', 'SLC', 'KIN', 'NAS', 'ATL', 'SDQ', 
    'MDE', 'SYR', 'CMW', 'RSW', 'CLE', 'SAN', 'PDX', 'LIR', 'JAX', 'STT', 
    'LRM', 'EWR', 'POP', 'ROC', 'AUA', 'BOS', 'BNA', 'LIM', 'PUJ', 'SWF', 
    'PVD']
    origN = flightName[orig]
    return render_template('submitted.html',
    	origN=orig,
    	lMonth=lMonth,
    	lDay=lDay,
    	lYear=lYear,
    	bMonth=bMonth,
    	bDay=bDay,
    	bYear=bYear)


if __name__ == "__main__":
    app.run()
