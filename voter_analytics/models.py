from django.db import models

import csv
from django.utils.dateparse import parse_date
import os

# Create your models here.

class Voter(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    street_number = models.IntegerField()
    street_name = models.CharField(max_length=200)
    apartment_number = models.CharField(max_length=50, blank=True, null=True)
    zip_code = models.CharField(max_length=10)
    date_of_birth = models.DateField()
    date_of_registration = models.DateField()
    party_affiliation = models.CharField(max_length=50)
    precinct_number = models.CharField(max_length=10)
    v20state = models.BooleanField()
    v21town = models.BooleanField()
    v21primary = models.BooleanField()
    v22general = models.BooleanField()
    v23town = models.BooleanField()
    voter_score = models.IntegerField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

def load_data():
    file_path = os.path.join(os.path.dirname(__file__), 'newton_voters.csv')
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            Voter.objects.create(
                first_name=row['First Name'],
                last_name=row['Last Name'],
                street_number=int(row['Residential Address - Street Number']),
                street_name=row['Residential Address - Street Name'],
                apartment_number=row.get('Residential Address - Apartment Number'),
                zip_code=row['Residential Address - Zip Code'],
                date_of_birth=parse_date(row['Date of Birth']),
                date_of_registration=parse_date(row['Date of Registration']),
                party_affiliation=row['Party Affiliation'],
                precinct_number=row['Precinct Number'],
                v20state=row['v20state'].strip().upper() == 'TRUE',
                v21town=row['v21town'].strip().upper() == 'TRUE',
                v21primary=row['v21primary'].strip().upper() == 'TRUE',
                v22general=row['v22general'].strip().upper() == 'TRUE',
                v23town=row['v23town'].strip().upper() == 'TRUE',
                voter_score=int(row['voter_score'])
            )
