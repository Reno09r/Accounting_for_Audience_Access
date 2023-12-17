from django.db import models

class Auditorium(models.Model):
    id = models.AutoField(primary_key=True)
    room_number = models.TextField()

    def __str__(self):
        return self.room_number

class Role(models.Model):
    id = models.AutoField(primary_key=True)
    role_name = models.TextField()
    is_master = models.BooleanField()

    def __str__(self):
        return self.role_name

class Employee(models.Model):
    id = models.AutoField(primary_key=True)
    role = models.ForeignKey(Role, on_delete=models.RESTRICT)
    first_name = models.TextField()
    last_name = models.TextField()
    birthday = models.DateField()
    email = models.TextField()
    phone = models.TextField()

    def __str__(self):
        return self.first_name, self.last_name

class IDCard(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.TextField()

    def __str__(self):
        return self.code

class EmployeeIDCard(models.Model):
    id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(Employee, on_delete=models.RESTRICT)
    IDCard = models.ForeignKey(IDCard, on_delete=models.RESTRICT)

class ByIDTakedKey(models.Model):
    id = models.AutoField(primary_key=True)
    IDCard = models.ForeignKey(EmployeeIDCard, on_delete=models.RESTRICT)
    auditorium = models.ForeignKey(Auditorium, on_delete=models.RESTRICT)
    take_time = models.DateTimeField()
    return_time = models.DateTimeField()
    is_returned = models.BooleanField()
    key_transferred = models.BooleanField()

    def __str__(self):
        return self.IDCard, self.auditorium

class Schedule(models.Model):
    id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(Employee, on_delete=models.RESTRICT)
    auditorium = models.ForeignKey(Auditorium, on_delete=models.RESTRICT)
    day_of_week = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

class KeyTransfer(models.Model):
    id = models.AutoField(primary_key=True)
    from_employee = models.ForeignKey(Employee, related_name='from_employee', on_delete=models.RESTRICT)
    to_employee = models.ForeignKey(Employee, related_name='to_employee', on_delete=models.RESTRICT)
    auditorium = models.ForeignKey(Auditorium, on_delete=models.RESTRICT)
    transfer_time = models.DateTimeField()

    def __str__(self) -> str:
        return self.from_employee, self.to_employee