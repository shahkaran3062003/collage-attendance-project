from django.db import models
# import uuid
import numpy as np
import os
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from api.settings import BASE_DIR


# Create your models here.


def student_img_path(instance, filename):

    return f"student/{instance.department}/{instance.year}/{instance.id}.jpg"


def generate_next_id():
    obj = Student.objects.all()
    if (obj):
        lastId = obj.order_by('id').last().id.split('-')[1]
        lastId = int(lastId)
        if (lastId <= 8):
            return f's-00{lastId+1}'
        elif (lastId <= 98):
            return f's-0{lastId+1}'

        else:
            return f's-{lastId+1}'

    else:
        return 's-001'


class Student(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id = models.CharField(
        primary_key=True, default=generate_next_id, editable=False, max_length=10)
    name = models.CharField(max_length=50)
    rollNumber = models.CharField(max_length=8)
    address = models.CharField(max_length=200)
    contact = models.PositiveBigIntegerField()
    email = models.EmailField(max_length=254)
    department = models.CharField(max_length=10)
    year = models.CharField(max_length=2)
    img = models.ImageField(upload_to=student_img_path)
    encodings = models.CharField(default=None, null=True, max_length=5000)

    def __str__(self):
        return f"{self.year}/{self.department}/{self.rollNumber}/{self.id}"

    def set_encodings(self, encodings):
        self.encodings = ",".join(str(e) for e in encodings)

    def get_encodings(self):
        return np.array([float(e) for e in self.encodings.split(',')])

    def delete_model(self, request, object):
        file = object.img
        os.remove(file)
        object.delete()


@receiver(pre_delete, sender=Student)
def delete_student_image(sender, instance: Student, **kwargs):
    if (instance.img):
        img_path = os.path.join(BASE_DIR, instance.img.path)
        os.remove(img_path)
