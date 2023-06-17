from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
# Create your models here.

class EmployeeDetail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    empcode = models.CharField(max_length=50)
    empdept = models.CharField(max_length=100, null=True)
    designation  = models.CharField(max_length=100, null=True)
    contact = models.IntegerField(null=True)
    gender = models.CharField(max_length=50, null=True)
    joiningdate = models.DateField(null=True)
    profile_image = models.ImageField(upload_to='employee_profiles/', null=True, default='default.png')

    def clean(self):
        super().clean()
        if self.profile_image:
            min_size_kb = 5  # minimum required file size in kilobytes
            max_size_kb = 50  # maximum allowed file size in kilobytes
            file_size = self.profile_image.size / 1024  # convert to KB
            if file_size < min_size_kb or file_size > max_size_kb:
                raise ValidationError(f"The profile image must be between {min_size_kb} KB and {max_size_kb} KB.")

    def __str__(self):
        return self.user.username

        


##Leave Managment System 


class Leave(models.Model):
    LEAVE_TYPES = (
        ('CL', 'Casual Leave'),
        ('EL', 'Earned Leave'),
        ('LWP', 'Leave Without Pay'),
        ('SL', 'Sick Leave'),
    )

    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=3, choices=LEAVE_TYPES)
    start_date = models.DateField()
    end_date = models.DateField()
    approved = models.BooleanField(default=False)
    reason = models.CharField(max_length=200)

    def get_duration(self):
        duration = self.end_date - self.start_date
        return duration.days + 1  # Add 1 to include both start and end dates

    def __str__(self):
        return f"{self.employee.username} - {self.leave_type}"

   



