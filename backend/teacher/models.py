from django.db import models
import numpy as np
import os
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from api.settings import BASE_DIR
# Create your models here.


def generate_next_id():
    obj = Teacher.objects.all()
    if (obj):
        lastId = obj.order_by('id').last().id.split('-')[1]
        lastId = int(lastId)
        if (lastId <= 8):
            return f't-00{lastId+1}'
        elif (lastId <= 98):
            return f't-0{lastId+1}'

        else:
            return f't-{lastId+1}'

    else:
        return 't-001'


def teacher_img_path(instance, filename):
    return f"teacher/{instance.department}/{instance.id}.jpg"


class Teacher(models.Model):
    id = models.CharField(
        primary_key=True, default=generate_next_id, editable=False, max_length=10)
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    contact = models.PositiveBigIntegerField()
    email = models.EmailField(max_length=254)
    department = models.CharField(max_length=10)
    img = models.ImageField(upload_to=teacher_img_path)
    encodings = models.CharField(default=None, null=True, max_length=5000)

    def set_encodings(self, encodings):
        self.encodings = ",".join(str(e) for e in encodings)

    def get_encodings(self):
        return np.array([float(e) for e in self.encodings.split(',')])

    def delete_model(self, request, object):
        file = object.img
        os.remove(file)
        object.delete()

    def __str__(self):
        return f"{self.department}-{self.name}/{self.id}"


@receiver(pre_delete, sender=Teacher)
def delete_student_image(sender, instance: Teacher, **kwargs):
    if (instance.img):
        img_path = os.path.join(BASE_DIR, instance.img.path)
        os.remove(img_path)
