from django.db import models
from django.urls import reverse


# Create your models here.

def load_data():
    """
    Function to load data records from CSV file into Django model instances.
    """

    Voter.objects.all().delete()

    filename = "voter_analytics/newton_voters.csv"
    f = open(filename)
    f.readline()

    for line in f:
        fields = line.split(',')
        try:
            voter = Voter(
                last_name = fields[1],
                first_name = fields[2],
                ad_st_num = fields[3], 
                ad_st_name = fields[4],
                ad_apt_num = fields[5],
                ad_zip_code = fields[6],
                dob = fields[7],
                do_reg = fields[8],
                part_af = fields[9],
                precint_num = fields[10],
                
                v20state = (fields[11] == "TRUE"),
                v21town = (fields[12] == "TRUE"),
                v21primary = (fields[13] == "TRUE"),
                v22general = (fields[14] == "TRUE"),
                v23town = (fields[15] == "TRUE"),

                voter_score = fields[16],
            )

            voter.save()
            print(f"Created voter: {voter}")

        except Exception as e:
            print(f"Skipped: {fields}")
            # print(f"Because of {e}")

class Voter(models.Model):
    """
    Data model for a individual voter.
    """

    last_name = models.CharField()
    first_name = models.CharField()
    ad_st_num = models.CharField()
    ad_st_name = models.CharField()
    ad_apt_num = models.CharField()
    ad_zip_code = models.CharField()
    dob = models.DateField()
    do_reg = models.DateField()
    part_af = models.CharField(max_length=2)
    precint_num = models.CharField()

    v20state = models.BooleanField()
    v21town = models.BooleanField()
    v21primary = models.BooleanField()
    v22general = models.BooleanField()
    v23town = models.BooleanField()

    voter_score = models.IntegerField()


    def __str__(self):
        return f"{self.first_name} {self.last_name}_{self.precint_num}"
    




