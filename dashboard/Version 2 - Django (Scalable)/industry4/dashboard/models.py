from django.db import models
from django.contrib.auth.models import User
import uuid
from datetime import datetime

class Process(models.Model):
    ProcessID = models.AutoField(primary_key=True, db_column='ProcessID')
    ProcessName = models.CharField(max_length=20, db_column='ProcessName')
    NumStations = models.PositiveSmallIntegerField(db_column='NumStations')
    ProcessDesc = models.CharField(max_length=255, db_column='ProcessDesc', null=True)
    DateCreated = models.DateField(db_column='DateCreated', null=True)
    TimesCompleted = models.PositiveSmallIntegerField(db_column='TimesCompleted', default=0)
    GoalTime = models.TimeField(db_column='GoalTime')
    AvgTime = models.TimeField(db_column='AvgTime')

    class Meta:
        db_table = 'process'
        verbose_name_plural = 'Processes'

    def __str__(self):
        return f'Process {str(self.ProcessName)}'



class Product(models.Model):
    ProductID = models.AutoField(primary_key=True, db_column='ProductID')
    ProcessID = models.ForeignKey(Process, on_delete=models.CASCADE, db_column='ProcessID')
    Completed = models.BooleanField(default=False, db_column='Completed')
    Accepted = models.BooleanField(default=False, db_column='Accepted')
    StartTime = models.DateTimeField(db_column='StartTime')
    EndTime = models.DateTimeField(db_column='EndTime')
    TotalTime = models.TimeField(db_column='TotalTime')

    class Meta:
        db_table = 'product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return f'Product {str(self.ProductID)}'
    
    # def save(self, *args, **kwargs):
    #     if self.Completed:
    #         self.EndTime = datetime.now()
    #         self.TotalTime = self.EndTime - self.StartTime
    #     super(Product, self).save(*args, **kwargs)




class ProductTime(models.Model):
    product_id = models.OneToOneField(Product, primary_key=True, on_delete=models.CASCADE, db_column='ProductID')
    station_one = models.TimeField(db_column='StationOne')
    station_two = models.TimeField(db_column='StationTwo')
    station_three = models.TimeField(db_column='StationThree')
    station_four = models.TimeField(db_column='StationFour')
    station_five = models.TimeField(db_column='StationFive')
    total_time = models.TimeField(db_column='TotalTime')

    class Meta:
        db_table = 'productTime'
        verbose_name_plural = 'Product Times'

    def __str__(self):
        return f'Product {str(self.product_id)}'



class Stations(models.Model):
    StationID = models.AutoField(primary_key=True, db_column='StationID')
    ProcessID = models.ForeignKey(Process, on_delete=models.CASCADE, db_column='ProcessID')
    NumSteps = models.PositiveSmallIntegerField(db_column='NumSteps')
    EstimatedTime = models.TimeField(db_column='EstimatedTime')
    DateCreated = models.DateField(db_column='DateCreated')
    StationDesc = models.CharField(max_length=255, db_column='StationDesc')
    AverageTime = models.TimeField(db_column='AverageTime')
    Active = models.BooleanField(default=False, db_column='Active')

    class Meta:
        db_table = 'stations'
        verbose_name_plural = 'Stations'

    def __str__(self):
        return f'Station {str(self.StationID)}'



class Steps(models.Model):
    StepID = models.AutoField(primary_key=True, db_column='StepID')
    StationID = models.ForeignKey(Stations, on_delete=models.CASCADE, db_column='StationID')
    StepDesc = models.CharField(max_length=255, db_column='StepDesc', null=True)
    PhotoLink = models.URLField(db_column='PhotoLink', null=True)
    InfoLink = models.URLField(db_column='InfoLink', null=True)

    class Meta:
        db_table = 'steps'
        verbose_name_plural = 'Steps'

    def __str__(self):
        return f'Step {str(self.StepID)}'



class StationHistory(models.Model):
    StatHistID = models.AutoField(primary_key=True, db_column='StatHistID')
    StationID = models.ForeignKey(Stations, on_delete=models.CASCADE, db_column='StationID')
    ProductID = models.ForeignKey(Product, on_delete=models.CASCADE, db_column='ProductID')
    Accepted = models.BooleanField(default=True, db_column='Accepted')
    DateCompleted = models.DateField(db_column='DateCompleted')
    TimeTaken = models.TimeField(db_column='TimeTaken')

    class Meta:
        db_table = 'StationHistory'
        verbose_name_plural = 'Station Histories'

    def __str__(self):
        return f'Station History {str(self.StatHistID)}'

