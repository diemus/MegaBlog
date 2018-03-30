from django.db import models

# Create your models here.

class SidebarNavItem(models.Model):
    path=models.CharField(max_length=32,unique=True)
    icon=models.CharField(max_length=32)
    caption=models.CharField(max_length=32,unique=True)
    STATUS_CHOICE={
        0:'未启用',
        1:'启用'
    }
    status=models.CharField(max_length=10,choices=STATUS_CHOICE.items(),default=0)