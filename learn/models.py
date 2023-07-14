from django.db import models


class User(models.Model):
    name = models.CharField(max_length=64)
    password = models.CharField(max_length=32)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'<Course:{self.name}>'


class UserDetails(models.Model):
    name = models.OneToOneRel(field='User', field_name='name', on_delete=models.CASCADE, to='')
    detail = models.CharField(max_length=256)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.detail


class Course(models.Model):
    name = models.CharField(max_length=64)
    pub_date = models.DateField()
    stu_number = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'<Course:{self.name}>'
