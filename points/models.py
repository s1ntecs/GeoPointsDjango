from django.db import models


class Part(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class PointFile(models.Model):
    file_name = models.CharField(max_length=255)

    def __str__(self):
        return self.file_name


class Point(models.Model):
    name = models.CharField(max_length=255)
    x = models.CharField(max_length=255, null=True, blank=True)
    y = models.CharField(max_length=255, null=True, blank=True)
    z = models.CharField(max_length=255, null=True, blank=True)
    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    point_file = models.ForeignKey(PointFile, on_delete=models.CASCADE,
                                   null=True,
                                   blank=True)
    row_number = models.IntegerField(null=True, blank=True)

    @property
    def coordinates(self):
        return {'X': self.x, 'Y': self.y, 'Z': self.z}

    def __str__(self):
        return self.name
