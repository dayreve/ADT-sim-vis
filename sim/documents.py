"""
This module contains all of functions to create appropriately structured documents
to insert data into the MongoDB database. All data is FHIR compliant or close to.
"""

import datetime


def create_ward(ward):

    ward = {
        'resourceType': 'Location',
        'identifier': ward.ward_id,
        'name': f'Ward{ward.ward_id}',
        'type': { 
            'specialty': str(ward.ward_type),
            'gender': ward.gender
        }
    }

    return ward


def create_bed(bed):

    bed = {
        'resourceType': 'Location',
        'identifier': bed.bed_id,
        'status': 'active',
        'partOf': {
            'wardIdentifier': bed.ward_id
        }
    }

    return bed


def create_patient(patient):
    """Output FHIR patient, takes Patient object"""

    pat = {
        'resourceType': 'Patient',
        'identifier': [
            {
                'hosp_no': patient.pat_no
            }
        ],
        'name': [
            {
                'family': patient.sname,
                'given': patient.fname
            }
        ],
        'birthDate': patient.dob,
        'gender': patient.gender,
        'estimatedDischarge': patient.edd
    }

    return pat


def create_admission(patient, bed, time):
    
    encounter = {
        "resourceType": "Encounter",
        "pat_no": patient.pat_no,
        "location": [
            {
                "location": {
                    "ward_id": bed.ward_id,
                    "bed_id": bed.bed_id
                },
                "period": {
                    "start": time
                }
            }
        ]
    }

    return encounter


def create_movement(encounter, bed, time):

    mvmt = {
        "location": {
            "ward_id": bed.ward_id,
            "bed_id": bed.bed_id
        },
        "period": {
            "start": time
        }
    }

    encounter["location"][-1]["period"]["end"] = time

    encounter["location"].append(mvmt)

    return encounter


def create_discharge(encounter, time):

    encounter["location"][-1]["period"]["end"] = time
    
    return encounter


def create_news(pat_no, news, time):

    news = {
        "resourceType": "Observation",
        "code": {
            "text": "NEWS"
        },
        "subject": {
            "reference": pat_no
        },
        "effectiveDateTime": time,
        "valueQuantity": {
            "value": news
        }
    }

    return news


def create_observation(obs):
    """Output FHIR standard observation, takes Observation object"""

    obs = {
        "resourceType": "Bundle",
        "entry": [
            {
                "resource": {
                    "resourceType": "Observation",
                    "text": "Respiratory Rate",
                    "effectiveDateTime": obs.datetime,
                    "subject": {
                        "reference": obs.pat_no
                    },
                    "valueQuantity": {
                        "value": obs.resp_rate,
                    }
                }
            },
            {
                "resource": {
                    "resourceType": "Observation",
                    "text": "Body Temperature",
                    "effectiveDateTime": obs.datetime,
                    "subject": {
                        "reference": obs.pat_no
                    },
                    "valueQuantity": {
                        "value": obs.temp,
                    }
                }
            },
            {
                "resource": {
                    "resourceType": "Observation",
                    "text": "BP Systolic",
                    "effectiveDateTime": obs.datetime,
                    "subject": {
                        "reference": obs.pat_no
                    },
                    "valueQuantity": {
                        "value": obs.bp_sys,
                    }
                }
            },
            {
                "resource": {
                    "resourceType": "Observation",
                    "text": "Heart Rate",
                    "effectiveDateTime": obs.datetime,
                    "subject": {
                        "reference": obs.pat_no
                    },
                    "valueQuantity": {
                        "value": obs.pulse,
                    }
                }
            }
        ]
    }

    return obs
