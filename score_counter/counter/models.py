from django.db import models

# Create your models here.
class MajorManager(models.Manager):
    def get_all(self):
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute('''
                SELECT * FROM counter_major
                ''')
            result_list = []
            for row in cursor.fetchall():
                p = self.model(college_num=row[0],year=row[1],college=row[2], \
                               number=row[3],name=row[4],score_pub=row[5],score_core=row[6], \
                               score_sele=row[7],score_dev=row[8],ps=row[9])
                result_list.append(p)
        return result_list

    def get_by_col(self,col):
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("""
                        SELECT %s FROM counter_major
                        """%col)
            result_list = []
            for row in cursor.fetchall():
                result_list.append(row[0])
        return result_list

    def get_with_value(self,col,value,col1='',value1=''):
        from django.db import connection
        a = str(col)+' = "'+str(value) +'"'
        if not col1=='':
            b = ' and '+str(col1)+' = "'+str(value1) +'"'
        else:
            b = ''
        sql = 'SELECT * FROM counter_major WHERE '+a+b+';'
        with connection.cursor() as cursor:
            cursor.execute(sql)
            result_list = []
            for row in cursor.fetchall():
                p = self.model(college_num=row[0], year=row[1], college=row[2], \
                               number=row[3], name=row[4], score_pub=row[5], score_core=row[6], \
                               score_sele=row[7], score_dev=row[8], ps=row[9])
                result_list.append(p)
        return result_list

class DetailManager(models.Manager):
    def get_all(self):
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute('''
                SELECT * FROM counter_detail
                ''')
            result_list = []
            for row in cursor.fetchall():
                p = self.model(id=row[0], number=row[1], name=row[2], point=row[3], type=row[4], class_num=row[5])
                result_list.append(p)
        return result_list

    def get_by_col(self,col):
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute('''
                        SELECT %s FROM counter_detail
                        '''%col)
            result_list = []
            for row in cursor.fetchall():
                result_list.append(row[0])
        return result_list

    def get_with_value(self,col,value):
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute('''
                                SELECT * FROM counter_detail
                                  WHERE %s = %s
                                ''' % (col,str(value)))
            result_list = []
            for row in cursor.fetchall():
                p = self.model(id=row[0], number=row[1], name=row[2], point=row[3], type=row[4], class_num=row[5])
                result_list.append(p)
        return result_list

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
    objects = MajorManager()

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
    objects = DetailManager()

    def export(self):
        self.data = [self.id,self.number,self.name,self.point,self.type,self.class_num]
        return self.data

    def __str__(self):
        self.export()
        this_str = ''
        for item in self.data:
            this_str = this_str+str(item) +' '
        return this_str