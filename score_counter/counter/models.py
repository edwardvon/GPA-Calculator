from django.db import models

# Create your models here.
class Major(models.Model):
    college_num = models.IntegerField()
    year = models.IntegerField()
    college = models.TextField()
    number = models.IntegerField(primary_key=True)
    name = models.TextField()
    score_pub = models.FloatField()
    score_core = models.FloatField()
    score_sele = models.FloatField()
    score_dev = models.FloatField()
    ps = models.TextField(null=True)

    def export(self):
        self.data = [self.college_num,self.year,self.college,self.number,self.name, \
                self.score_pub,self.score_core,self.score_sele,self.score_dev,self.ps]
        return self.data

    def __str__(self):
        self.export()
        this_str = ''
        for i in range(0,5):
            this_str = this_str + str(self.data[i])+' '
        return this_str

class Detail(models.Model):
    id = models.IntegerField(primary_key=True)
    number = models.CharField(max_length=10)
    name  = models.TextField()
    point = models.FloatField()
    type = models.IntegerField()
    class_num = models.IntegerField()

    def export(self):
        self.data = [self.id,self.number,self.name,self.point,self.type,self.class_num]
        return self.data

    def __str__(self):
        self.export()
        this_str = ''
        for item in self.data:
            this_str = this_str+str(item) +' '
        return this_str