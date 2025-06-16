from django.db import models
from app.models.Project import Project
from app.models.UsState import UsState
from app.models.MacAddress import MacAddress
from app.models.Node import Node
from app.models.User import User

class Home(models.Model):
    home_id = models.AutoField(primary_key=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=10)
    unit = models.CharField(max_length=50, blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    node_switch_unit = models.IntegerField(blank=True, null=True)
    node_switch_module = models.IntegerField(blank=True, null=True)
    node_port_num = models.IntegerField(blank=True, null=True)
    wiring_certified_on = models.DateTimeField(blank=True, null=True)
    exclude_from_reports = models.BooleanField(default=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, db_column='project_id')
    state = models.ForeignKey(UsState, on_delete=models.CASCADE, db_column='state_id')
    node = models.ForeignKey(Node, on_delete=models.CASCADE, db_column='node_id', related_name='homes')
    wiring_certified_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='certified_wirings', db_column='wiring_certified_by')
    subscribers = models.ManyToManyField('Subscriber', through='MultiHomeSubscriberHome', related_name='homes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = "homes"
        ordering = ['address']
    def __str__(self):
        return self.address
    @property
    def active_subscriber(self):
        return self.subscribers.filter(
            service_activated_on__isnull=False,
            service_deactivated_on__isnull=True
        ).exclude(service_plan_id=1).first()