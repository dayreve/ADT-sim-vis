from enum import Enum


class WardType(Enum):
    GENERAL = 1
    SURGERY = 2
    MATERNITY = 3
    PAEDIATRIC = 4
    ENT = 5
    GASTRO = 6


class Ward:

    def __init__(self, ward_id, beds, ward_type, gender):
        self.ward_id = ward_id
        self.beds = beds
        self.ward_type = ward_type
        self.gender = gender


class Bed:

    def __init__(self, bed_id, ward):
        self.bed_id = bed_id
        self.ward_id = ward.ward_id
        self.occupied = False


class Observation:

    def __init__(self):
        self.datetime = ''
        self.pat_no = ''
        self.resp_rate = ''
        self.o2_sats = ''
        self.temp = ''
        self.bp_sys = ''
        self.pulse = ''
        self.consciousness = ''
        

class Patient:

    def __init__(self, **kwargs):
        self.fname = kwargs.get('fname')
        self.sname = kwargs.get('sname')
        self.dob = kwargs.get('dob')
        self.gender = kwargs.get('gender')
        self.pat_no = kwargs.get('pat_no')
        self.inpatient = False
        self.edd = kwargs.get('edd')
