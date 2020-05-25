from django.db import models


# Create your models here.
import os

os.environ['DYLD_LIBRARY_PATH'] = '/Library/PostgreSQL/12/lib'


class Brand_Generic_Otc(models.Model):
    gdc = models.TextField()
    item_identifier = models.TextField()
    description = models.TextField()
    rx_otc = models.TextField()
    generic_brand = models.TextField()
    schedule = models.TextField()
    package_size = models.FloatField()
    manufacturer = models.TextField()


class Transaction_Table(models.Model):
    # id = models.IntegerField(primary_key=True)
    date_filled = models.DateField()
    rxnumber = models.TextField()
    ndc = models.TextField()
    description = models.TextField()
    qty_dispensed = models.FloatField()
    primary_amt = models.FloatField()
    secondary_amt = models.FloatField()
    patient_copay = models.FloatField()
    total_sales = models.FloatField()
    acquisition_costs = models.FloatField()
    profit = models.FloatField()
    margin = models.FloatField()
    dawcode = models.TextField()
    drug_manufacturer = models.TextField()
    acq_unit_cost = models.FloatField()
    gdc = models.TextField()
    status = models.TextField()
    generic = models.TextField()


class Dashboard_Page_Table(models.Model):
    gcn = models.TextField()
    description = models.TextField()
    volume = models.FloatField()
    total_revenue = models.FloatField()
    total_cost = models.FloatField()
    profit = models.FloatField()
    margin = models.FloatField()
    unit_cost = models.FloatField()
    alternative_unit_cost = models.FloatField()
    savinsg_with_alternative_unit_cost = models.FloatField()
    drug_manufacturer = models.TextField()
    date_filled = models.TextField()


    class Meta:
        ordering = ('gdc',)
