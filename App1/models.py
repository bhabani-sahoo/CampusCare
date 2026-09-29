from django.db import models
from django.contrib.auth.models import User
# Create your models here.
COMPLAINT_CHOICES=[("Academic","Academic"),
                 ("Infrastructure","Infrastructure"),
                 ("Hostel","Hostel"),
                 ("Library","Library"),
                 ("Transport","Transport"),
                 ("Fees & Accounts","Fees & Accounts")]
STATUS_CHOICES = [
    ('Pending', 'Pending'),
    ('In Progress', 'In Progress'),
    ('Resolved', 'Resolved'),
    ('Rejected', 'Rejected'),
]
SATISFACTION_CHOICES=[
    ('Pending', 'Pending'),
    ('Satisfied','Satisfed'),
    ('Non-satisfied','Non-satisfied'),
]
GENDER_CHOICES=[("Male","Male"),
                ("Female","Female")]
class Complains(models.Model):
    student=models.ForeignKey(User,on_delete=models.CASCADE)
    complaint_catagory=models.CharField(max_length=25,choices=COMPLAINT_CHOICES)
    description = models.TextField(max_length=250)
    complaint_id = models.CharField(
        max_length=20,
        unique=True,
        editable=True
    )
    def save(self, *args, **kwargs):
        if not self.complaint_id:
            last_complaint = Complains.objects.order_by('-id').first()
            if last_complaint:
                last_id = int(last_complaint.complaint_id[3:])
                new_id = last_id + 1
            else:
                new_id = 1
            self.complaint_id = f"CMP{new_id:04d}"
        super().save(*args, **kwargs)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    status=models.CharField(max_length=23,default='Pending',choices=STATUS_CHOICES)
    file=models.FileField(
        upload_to="complaint_files/",
        blank=True,
        null=True
    )
    image=models.ImageField(
        upload_to="Complaint_image",
        blank=True,
        null=True
    )
    remark=models.TextField(
        blank=True,
        null=True
    )
    satisfaction=models.CharField(
        max_length=20,
        choices=SATISFACTION_CHOICES,
        default="Pending"
    )
    branch=models.CharField(max_length=30,blank=True,null=True)
    batch=models.CharField(max_length=20,blank=True,null=True)
    Gender=models.CharField(max_length=10,blank=True,null=True)
    def __str__(self):
        return self.complaint_id

class StudentProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    batch = models.CharField(max_length=20)
    Roll=models.CharField(max_length=20 ,default="Null")
    branch=models.CharField(max_length=30,blank=True,null=True)
    is_hosteler = models.BooleanField(default=False)
    gender = models.CharField(
    max_length=10,
    choices=GENDER_CHOICES,blank=True,null=True)
    def save(self, *args, **kwargs):
        if self.branch:
            self.branch = self.branch.upper()

        super().save(*args, **kwargs)
    def __str__(self):
        return self.user.username