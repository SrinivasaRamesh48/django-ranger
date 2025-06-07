from django.db import models
from app.models.PortMacAddress import PortMacAddress 

class Home(models.Model):
    home_id = models.AutoField(primary_key=True)

    project = models.ForeignKey('Project', on_delete=models.SET_NULL, null=True, db_column='project_id', related_name='homes')
    us_state = models.ForeignKey('UsState', on_delete=models.SET_NULL, null=True, db_column='state_id', related_name='homes')
    mac_address = models.ForeignKey('MacAddress', on_delete=models.SET_NULL, null=True, db_column='mac_address_id', related_name='homes')
    node = models.ForeignKey('Node', on_delete=models.SET_NULL, null=True, db_column='node_id', related_name='homes')
    wiring_certified_by = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, db_column='wiring_certified_by', related_name='certified_homes')

    # Fields
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    unit = models.CharField(max_length=50, null=True, blank=True)
    subsciber = models.CharField(max_length=255, null=True, blank=True)  # Typo retained as per original
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    node_switch_unit = models.IntegerField(null=True, blank=True)
    node_switch_module = models.IntegerField(null=True, blank=True)
    node_port_num = models.IntegerField(null=True, blank=True)

    wiring_certified_on = models.DateField(null=True, blank=True)
    exclude_from_reports = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'homes'


    def ont(self):
        return self.ont_set.first()

    def mesh_installs(self):
        return self.meshcpeinstall_set.filter(deleted_at__isnull=True)

    def subscribers(self):
        return self.subscriber_set.all()

    def active_subscriber(self):
        return self.subscriber_set.filter(
            service_activated_on__isnull=False,
            service_deactivated_on__isnull=True
        ).exclude(service_plan_id=1).first()

    def multi_home_subscriber(self):
        return self.multihomesubscriberhome_set.first()

    def uploads(self):
        return self.uploads_set.all()

    def alerts(self):
        return self.homealert_set.filter(active=True).order_by('-alert_type__id')

    def port_mac_address(self):
        
        return PortMacAddress.objects.filter(
            node_id=self.node_id,
            node_switch_unit=self.node_switch_unit,
            node_switch_module=self.node_switch_module,
            node_port_num=self.node_port_num
        ).select_related('mac_address_found').first()
