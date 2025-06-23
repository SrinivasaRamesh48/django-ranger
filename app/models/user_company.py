from django.db import models

class UserCompany(models.Model):
    user_company_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)


    class Meta:
        db_table = 'user_companies'
        app_label = 'app'

    def __str__(self):
        return self.name or f"User Company {self.user_company_id}"