from django.db import models

# Create your models here.
class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    class Meta:
        managed = True
        db_table = 'category'

class Country(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False)
    iso_code = models.CharField(max_length=2, null=False)

    class Meta:
        managed = True
        db_table = 'country'

class State(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False)
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, db_constraint=False, db_index=True
    )
    class Meta:
        managed = True
        db_table = 'state'

class Vendors(models.Model):
    id = models.AutoField(primary_key=True)
    display_name = models.CharField(max_length=200, null=False)
    latitude = models.CharField(max_length=200)
    longitude = models.CharField(max_length=200)
    sample_delivery = models.BooleanField(default=False)
    virtual_assistance = models.BooleanField(default=False)
    open_slot = models.TextField(max_length=200)
    address = models.TextField(max_length=200)
    image = models.TextField(max_length=2000)
    ratings = models.IntegerField()
    country = models.ForeignKey(
        Country, on_delete=models.DO_NOTHING, db_constraint=False, db_index=True
    )
    state = models.ForeignKey(
        State, on_delete=models.DO_NOTHING, db_constraint=False, db_index=True
    )
    class Meta:
        managed = True
        db_table = 'vendors'


class Products(models.Model):
    id = models.AutoField(primary_key=True)
    display_name = models.CharField(max_length=200, null=False)
    style = models.CharField(max_length=150)
    kind = models.CharField(max_length=250)
    dimension = models.CharField(max_length=2000)
    image = models.CharField(max_length=1500, null=False)
    category = models.ForeignKey(
        Category, on_delete=models.DO_NOTHING, db_constraint=False, db_index=True
    )
    vendor = models.ForeignKey(
        Vendors, on_delete=models.DO_NOTHING, db_constraint=False, db_index=True
    )
    class Meta:
        managed = True
        db_table = 'products'

class Rating(models.Model):
    id = models.AutoField(primary_key=True)
    value = models.IntegerField(null=False)
    product = models.ForeignKey(
        Products, on_delete=models.DO_NOTHING, db_constraint=False, db_index=True
    )
    vendor = models.ForeignKey(
        Vendors, on_delete=models.DO_NOTHING, db_constraint=False, db_index=True
    )
    class Meta:
        managed = True
        db_table = 'rating'

class Stock(models.Model):
    id = models.AutoField(primary_key=True)
    status = models.BooleanField(default=True)
    product = models.ForeignKey(
        Products, on_delete=models.DO_NOTHING, db_constraint=False, db_index=True
    )
    vendor = models.ForeignKey(
        Vendors, on_delete=models.DO_NOTHING, db_constraint=False, db_index=True
    )
    class Meta:
        managed = True
        db_table = 'stock'

class Price(models.Model):
    id = models.AutoField(primary_key=True)
    currency = models.CharField(max_length=200)
    amount = models.IntegerField()
    product = models.ForeignKey(
        Products, on_delete=models.DO_NOTHING, db_constraint=False, db_index=True
    )
    vendor = models.ForeignKey(
        Vendors, on_delete=models.DO_NOTHING, db_constraint=False, db_index=True
    )
    country = models.ForeignKey(
        Country, on_delete=models.DO_NOTHING, db_constraint=False, db_index=True
    )
    state = models.ForeignKey(
        State, on_delete=models.DO_NOTHING, db_constraint=False, db_index=True
    )
    class Meta:
        managed = True
        db_table = 'price'
