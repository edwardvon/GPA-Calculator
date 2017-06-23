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

    def get_scorerequest(self,class_num):
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute('''
                        SELECT * FROM counter_major WHERE number=%d
                        '''%class_num)
            for row in cursor.fetchall():
                p = self.model(score_pub=row[5], score_core=row[6],score_sele=row[7], score_dev=row[8], ps=row[9])
        return p

class DetailManager(models.Manager):
    def get_all(self):
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute('''
                SELECT * FROM counter_detail
                ''')
            result_list = []
            for row in cursor.fetchall():
                p = self.model(id=row[0], number=row[1], name=row[2], point=row[3], \
                               type=row[4], class_num=row[5],if_complete=row[6])
                result_list.append(p)
        return result_list

class ScoreManager(models.Manager):
    def get_all(self):
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute('''
                SELECT * FROM counter_score
                ''')
            result_list = []
            for row in cursor.fetchall():
                p = self.model(id=row[0], term=row[1], number=row[2], name=row[3], type_c=row[12], \
                               point=row[4], get_point=row[5], grade=row[6], gpa=row[7], \
                               gpa_t=row[8], type=row[9],stu_num=row[10],class_num=row[11])
                result_list.append(p)
        return result_list

    def score_init(self,row):
        obj = Score.objects.filter(stu_num=row[9],term=row[0],number=row[1])
        if len(obj)==0:
            Score.objects.create(term=row[0], number=row[1], name=row[2], type_c=row[3],\
                       point=row[4], get_point=row[5], grade=row[6], gpa=row[7],\
                       gpa_t=row[8], stu_num=row[9], class_num=row[10],type=3)
        else:
            obj.update(type=3)
        return 1

    def get_gpa(self,stu_num):
        result = Score.objects.filter(stu_num=stu_num)
        point = sum(i.point for i in result)
        gpa_total = sum(i.gpa_t for i in result)
        return gpa_total/point

class MajorScoreManager(models.Manager):
    def get_all(self):
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute('''
                SELECT * FROM counter_majorscore
                ''')
            result_list = []
            for row in cursor.fetchall():
                p = self.model(id=row[0], lesson_num=row[1], lesson_name=row[2], point=row[3], type=row[4], \
                               class_num=row[5], stu_num=row[6], grade=row[7], if_complete=row[8])
                result_list.append(p)
        return result_list

    def majorscore_init(self,stu_number,class_number):
        request_list = Detail.objects.filter(class_num=class_number)
        for item in request_list:
            obj = MajorScore.objects.filter(lesson_num=item.number, lesson_name=item.name, stu_num=stu_number)
            if len(obj)==0:
                MajorScore.objects.create(lesson_num=item.number, lesson_name=item.name, point=item.point,\
                                           type=item.type, class_num=class_number, stu_num=stu_number,\
                                           if_complete=0)
            else:
                obj.update(grade=0,if_complete=0)
        return 1

    def majorscore_join(self,stu_number):
        request_list = MajorScore.objects.filter(stu_num=stu_number,type__lte=2)
        for item in request_list:
            if item.lesson_num=='53000100':
                continue
            a = []
            com = 1
            grades = Score.objects.filter(number__contains=item.lesson_num[:6],stu_num=stu_number)
            if not len(grades)==0:
                for i in grades:
                    a.append(i.grade)
                    Score.objects.filter(id=i.id).update(type=item.type)
            else:
                a = [0]
            if min(a)=='F' or min(a)==0:
                com = 0
            MajorScore.objects.filter(id=item.id).update(grade=min(a), if_complete=com)
        pe_list = MajorScore.objects.filter(lesson_num='53000100',stu_num=stu_number)
        pe_grades = Score.objects.filter(number__startswith='530001',stu_num=stu_number)
        for i in range(len(pe_grades)):
            com = 1
            id = pe_list[i].id
            gra = pe_grades[i].grade
            if gra=='F' or gra==0:
                com = 0
            Score.objects.filter(id=pe_grades[i].id).update(type=1)
            MajorScore.objects.filter(id=id).update(grade=gra,if_complete=com)
        return 1

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
    if_complete = models.BooleanField(default=0)
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


class Score(models.Model):
    id = models.IntegerField(primary_key=True)
    term = models.IntegerField()
    number = models.CharField(max_length=10)
    name = models.TextField()
    type_c = models.TextField()
    point = models.FloatField()
    get_point = models.FloatField()
    grade = models.CharField(max_length=3)
    gpa = models.FloatField()
    gpa_t = models.FloatField()
    type = models.IntegerField()
    stu_num = models.IntegerField()
    class_num = models.IntegerField()
    objects = ScoreManager()

    def export(self):
        self.data = [self.term,self.number,self.name,self.type_c,self.point, \
                self.get_point,self.grade,self.gpa,self.gpa_t,self.stu_num,self.class_num]
        return self.data

    def __str__(self):
        self.export()
        this_str = ''
        for i in range(0,11):
            this_str = this_str + str(self.data[i])+' '
        return this_str

class MajorScore(models.Model):
    id = models.IntegerField(primary_key=True)
    lesson_num = models.CharField(max_length=10)
    lesson_name = models.TextField()
    point = models.FloatField()
    type = models.IntegerField()
    class_num = models.IntegerField()
    stu_num = models.IntegerField()
    grade = models.CharField(max_length=3, null=False)
    if_complete = models.BooleanField(default=0)
    objects = MajorScoreManager()