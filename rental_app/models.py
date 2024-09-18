from django.db import models

# Create your models here.

class Admin(models.Model):
    username = models.CharField(max_length=60,primary_key=True)
    password = models.CharField(max_length=60)


class User(models.Model):
    userId = models.AutoField(primary_key=True)
    fullName = models.CharField(max_length=60)
    
    address = models.CharField(max_length=250)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15)
    aadharNumber=models.CharField(max_length=15)
    password = models.CharField(max_length=50)
    userPic = models.CharField(max_length=150)
    registerDate = models.DateField(auto_now_add=True)
    USER_TYPES = (
        ('Landlord', 'Landlord'),
        ('Tenant', 'Tenant'),
    )
    userType = models.CharField(max_length=50, choices=USER_TYPES)


class HouseDetails(models.Model):
    houseId = models.AutoField(primary_key=True)
    landLordId = models.IntegerField()
    registerDate = models.CharField(max_length=20)
    address = models.CharField(max_length=250)
    cityName = models.CharField(max_length=60)
    houseType = models.CharField(max_length=60)
    houseName = models.CharField(max_length=60)
    floorNumber = models.CharField(max_length=60)
    numberOfBedRooms = models.CharField(max_length=60)
    numberOfBathRooms = models.CharField(max_length=60)
    squareFeet = models.CharField(max_length=60)
    houseDescription = models.CharField(max_length=60)
    utilitiesDescription = models.CharField(max_length=60)
    houseImage = models.CharField(max_length=60)
    nearByEmenities = models.CharField(max_length=60)
    
    rentPrice = models.CharField(max_length=60)
    status = models.CharField(max_length=60)

    def __str__(self):
        return f"{self.houseName} - {self.address}"

    class Meta:
        db_table = 'HouseDetails'
