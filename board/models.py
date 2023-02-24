from django.db import models
from acc.models import User

# Create your models here.

class Board(models.Model):
    title = models.CharField(max_length=10)
    writer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="writer")
    course = models.CharField(max_length=10)
    date = models.DateTimeField()
    hour = models.CharField(max_length=10)
    min = models.CharField(max_length=10)
    cname = models.CharField(max_length=10)
    pee = models.CharField(max_length=10)
    jo = models.CharField(max_length=10)
    join_count = models.IntegerField(default=0)
    memo = models.CharField(max_length=30)
    sell = models.CharField(max_length=10)
    bname = models.CharField(max_length=10)
    rg = models.CharField(max_length=10,default='')
    gn = models.CharField(max_length=10)
    rq = models.CharField(max_length=10)
    etc = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.writer}_{self.rg}_{self.gn} (타임 로그)"

class Joinlook(models.Model):
    board = models.ForeignKey(Board,on_delete=models.CASCADE)
    j_writer = models.ForeignKey(User,on_delete=models.CASCADE)
    j_name = models.CharField(max_length=10)
    j_tag = models.CharField(max_length=10)
    j_count = models.CharField(max_length=10)
    join_count = models.IntegerField(blank=True, null=True)
    deposit_request = models.BooleanField(default=False)
    deposit_status = models.BooleanField(default=False)
    refund_request = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.board}_{self.j_writer}_{self.j_name}_{self.j_tag} (조인 로그)"
    
class SalaryRecord(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    year = models.IntegerField(blank=True, null=True)
    month = models.IntegerField(blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    join_count = models.IntegerField(blank=True, null=True)