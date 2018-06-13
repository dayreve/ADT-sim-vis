import sys
sys.path.insert(0, '..')

import database
import random
import datetime
from copy import deepcopy


def get_data():

    labels = ['Ward 1', 'Ward 2', 'Ward 3', 'Ward 4', 'Ward 5', 'Ward 6', 'Discharged']
    colours = ['red', 'orange', 'yellow', 'green', 'blue', 'purple', 'grey']


    data = {
        'node': {
            'label': labels * 2,
            'color': colours * 2
        },
        'link': {
            'source': [],
            'target': [],
            'value': []
        }
    }


    vs = [
        dict(zip(range(7), [0]*7)),
        dict(zip(range(7), [0]*7)),
        dict(zip(range(7), [0]*7)),
        dict(zip(range(7), [0]*7)),
        dict(zip(range(7), [0]*7)),
        dict(zip(range(7), [0]*7))
    ]

    dic = dict(zip(range(1, 7), vs))

    for i in range(database.PATIENTS.count()):

        e = database.ENCOUNTERS.find_one({'pat_no': f'PAT{i+1}'})['location']

        if 'end' in e[-1]['period']:
            dic[e[0]['location']['ward_id']][0] += 1

        else:
            dic[e[0]['location']['ward_id']][e[-1]['location']['ward_id']] += 1


    for k, v in dic.items():
        for l, w in v.items():
            if w > 0:
                data['link']['source'].append(k-1)
                data['link']['target'].append(l+6)
                data['link']['value'].append(w)

    return data


def get_interval_data(interval):

    labels = ['Discharged', 'Ward 1', 'Ward 2', 'Ward 3', 'Ward 4', 'Ward 5', 'Ward 6']
    colours = ['grey', 'red', 'orange', 'yellow', 'green', 'blue', 'purple']

    data = {
        'node': {
            'label': labels * 4,
            'color': colours * 4
        },
        'link': {
            'source': [],
            'target': [],
            'value': []
        }
    }

    value_dict = dict(zip(range(1, 7), [
        dict(zip(range(7), [0]*7)),
        dict(zip(range(7), [0]*7)),
        dict(zip(range(7), [0]*7)),
        dict(zip(range(7), [0]*7)),
        dict(zip(range(7), [0]*7)),
        dict(zip(range(7), [0]*7))
    ]))

    dic = {
        0: deepcopy(value_dict),
        1: deepcopy(value_dict),
        2: deepcopy(value_dict)
    }

    start_time = database.ENCOUNTERS.find_one({'pat_no': 'PAT1'})['location'][0]['period']['start']
    interval_hrs = interval

    for i in range(database.PATIENTS.count()):

        e = database.ENCOUNTERS.find_one({'pat_no': f'PAT{i+1}'})['location']

        start_index = 0
        end_index = 0

        for j in range(3):

            if end_index == -1 or len(e) == start_index:
                break

            for k in range(start_index, len(e)):
                if 'end' in e[k]['period']:
                    if e[k]['period']['end'] > start_time + datetime.timedelta(hours=(interval_hrs * j) + interval_hrs):
                        end_index = k
                        break
                
                end_index = -1 # if no entries past time interval use last element

            if 'end' in e[end_index]['period']:
                dic[j][e[start_index]['location']['ward_id']][0] += 1 # 0 index = discharged

            else:
                dic[j][e[start_index]['location']['ward_id']][e[end_index]['location']['ward_id']] += 1

            start_index = end_index + 1


    for k, v in dic.items():
        for l, w in v.items():
            for m, x in w.items():
                if x > 0:
                    data['link']['source'].append((k * 7) + l)
                    data['link']['target'].append(((k + 1) * 7) + m)
                    data['link']['value'].append(x)

    return data
