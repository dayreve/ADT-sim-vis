import sys
sys.path.insert(0, '..')

import random
import datetime
from time import sleep

import database
import documents
import entities
import randomdata


patients = []
wards = []
beds = []
current_pat_id = 0

ws = 6 # wards
bs = 5 # beds per ward
ps = 20 # initial patients


def free_beds():
    return [b for b in beds if not b.occupied]


def admissions(n, c):
    new_pats = []

    for _ in range(n):
        c += 1
        gender = randomdata.random_gender()
        new_pats.append(entities.Patient(**{
            'gender': gender,
            'fname': randomdata.random_male() if gender == 'male' else randomdata.random_female(),
            'sname': randomdata.random_surname(),
            'dob': randomdata.random_dob(),
            'pat_no': f'PAT{c}',
            'edd': randomdata.random_edd()
        }))

    for pat in new_pats:
        database.PATIENTS.insert_one(documents.create_patient(pat))
        bed = random.choice(free_beds())
        database.ENCOUNTERS.insert_one(documents.create_admission(pat, bed, datetime.datetime.now()))
        bed.occupied = True
        pat.inpatient = True

    patients.extend(new_pats)

    return n


database.WARDS.drop()
for i in range(ws):
    ward = entities.Ward(i+1, 5, entities.WardType(i+1), 'mixed')
    wards.append(ward)
    database.WARDS.insert_one(documents.create_ward(ward))

print(f'{ws} wards created')


database.BEDS.drop()
for w in wards:
    for i in range(bs):
        bed = entities.Bed((w.ward_id-1)*5 + i+1, w)
        beds.append(bed)
        database.BEDS.insert_one(documents.create_bed(bed))

print(f'{bs} beds created per ward')


database.PATIENTS.drop()
database.ENCOUNTERS.drop()
database.OBS.drop()
current_pat_id += admissions(ps, current_pat_id)
print(f'{ps} patients created and admitted')


sim_time = datetime.datetime.now()
for _ in range(30): # 100 iterations @ 15 mins interval ~= 24hrs
# while True:
#     sleep(1)

    sim_time += datetime.timedelta(minutes=15)

    events = {
        'discharges': 0,
        'movements': 0,
        'admissions': 0,
        'observations': 0
    }

    for p in [p for p in patients if p.inpatient == True]:

        if random.random() < 0.1:

            old_encounter = database.ENCOUNTERS.find_one({ 'pat_no': p.pat_no })
            old_bed_id = old_encounter['location'][-1]['location']['bed_id']
            old_bed = next(b for b in beds if b.bed_id == old_bed_id)
            old_bed.occupied = False

            if random.random() < 0.5:
                database.ENCOUNTERS.replace_one(
                    { 'pat_no': p.pat_no },
                    documents.create_discharge(old_encounter, sim_time)
                )

                p.inpatient = False
                events['discharges'] += 1

            else:
                bed = random.choice(free_beds())
                bed.occupied = True

                database.ENCOUNTERS.replace_one(
                    { "pat_no": p.pat_no },
                    documents.create_movement(old_encounter, bed, sim_time)
                )

                events['movements'] += 1

        else:

            database.OBS.insert_one(documents.create_news(p.pat_no, randomdata.random_news(), sim_time))
            events['observations'] += 1


    if random.random() < 0.25:

        num_free_beds = len(free_beds())
        a = random.choice(range(num_free_beds))
        current_pat_id += admissions(a, current_pat_id)
        events['admissions'] += a


    print(f'''
    {sim_time}
    Observations = {events['observations']}
    Admissions = {events['admissions']}
    Discharges = {events['discharges']}
    Movements = {events['movements']}
    Inpatients = {len([p for p in patients if p.inpatient == True])}
    Inpatients + outpatients = {len(patients)}
    ''')
