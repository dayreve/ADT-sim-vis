from flask import Flask, request, render_template, jsonify
from flask_pymongo import PyMongo
from plots.sankey import plot
from database import URI, DB_NAME
from datetime import date


app = Flask(__name__)
app.config['MONGO_DBNAME'] = DB_NAME
app.config['MONGO_URI'] = URI

mongo = PyMongo(app)


@app.route('/')
def index():
    return render_template('index.html', pixi='pixi-mixed-layout.js', sankey_selector=False, plot=plot(-1))

@app.route('/sankey')
def sankey():
    return render_template('index.html', pixi='', sankey_selector=True, plot=plot(2))

@app.route('/sankey/6')
def sankey2():
    return render_template('index.html', pixi='', sankey_selector=True, plot=plot(2))

@app.route('/sankey/12')
def sankey4():
    return render_template('index.html', pixi='', sankey_selector=True, plot=plot(4))

@app.route('/sankey/24')
def sankey8():
    return render_template('index.html', pixi='', sankey_selector=True, plot=plot(8))

@app.route('/movement')
def movement():
    return render_template('index.html', pixi='pixi-solo-layout.js', sankey_selector=False, plot='')


@app.route('/api/data', methods=['GET'])
def data():

    encounters = mongo.db.encounters.find()
    patients_db = mongo.db.patients
    obs_db = mongo.db.observations

    rtn = dict(zip(range(1, 31), [0]*30))
    free_beds = list(range(1, 31))

    for e in encounters:
        if 'end' not in e['location'][-1]['period']:
            bed_id = e['location'][-1]['location']['bed_id']

            pat_no = e['pat_no']
            pat = patients_db.find_one({'identifier': [{'hosp_no': pat_no}]})

            pat_obs = list(obs_db.find({'subject': {'reference': pat_no}}))
            news = (pat_obs[-1]['valueQuantity']['value'] if len(pat_obs) > 0 else 0)

            edd_y, edd_m, edd_d = map(int, pat['estimatedDischarge'].split('-'))
            edd = date(edd_y, edd_m, edd_d)

            fname = pat['name'][0]['family']
            sname = pat['name'][0]['given']

            pat_info = {
                'patNo': pat_no,
                'name': f'{fname}, {sname}',
                'dob': pat['birthDate'],
                'gender': pat['gender'],
                'news': news,
                'edd': edd,
                'lateDischarge': True if edd < date.today() and news < 5 else False,
                'potentialLateDischarge': True if edd == date.today() and news > 4 else False
            }

            rtn[bed_id] = pat_info
            free_beds = list(filter(lambda x: x != bed_id, free_beds))

    for b in free_beds:
        rtn[b] = 0

    return jsonify(rtn)


@app.route('/api/movements', methods=['GET'])
def movements():

    movements = {}

    for i in range(6):
        for j in range(i+1, 6):
            movements[f'{i+1}{j+1}'] = 0

    encounters = mongo.db.encounters.find()
    for e in encounters:
        x = e['location']

        for i in range(len(x)-1):

            a = x[i]['location']['ward_id']
            b = x[i+1]['location']['ward_id']

            if a < b:
                movements[f'{a}{b}'] += 1

            if b < a:
                movements[f'{b}{a}'] += 1

    return jsonify(movements)


if __name__ == '__main__':
    app.run()  # debug=True
