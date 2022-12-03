from django.db import models
import uuid

# Create your models here.


def student_img_path(instance, filename):

    return f"student/{instance.department}/{instance.year}/{instance.id}.jpg"


class Student(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    rollNumber = models.CharField(max_length=8)
    address = models.CharField(max_length=200)
    contact = models.PositiveBigIntegerField()
    email = models.EmailField(max_length=254)
    department = models.CharField(max_length=10)
    year = models.CharField(max_length=2)
    img = models.ImageField(upload_to=student_img_path)

    def __str__(self):
        return f"{self.year}/{self.department}/{self.rollNumber}"
