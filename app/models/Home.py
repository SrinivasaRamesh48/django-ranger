from django.db import models
from .mesh_cpe_install import MeshCPEInstall
from .ont import Ont
from .multi_home_subscriber_home import MultiHomeSubscriberHome
from .subscriber import Subscriber
from .uploads import Uploads
from .home_alert import HomeAlert
from .port_mac_address import PortMacAddress
class Home(models.Model):
    home_id = models.AutoField(primary_key=True)

    project = models.OneToOneField('Project', on_delete=models.SET_NULL, null=True, db_column='project_id')
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    us_state = models.OneToOneField('UsState', on_delete=models.SET_NULL, null=True, db_column='state_id')
    zip_code = models.CharField(max_length=20)
    unit = models.CharField(max_length=50, null=True, blank=True)
    subsciber = models.CharField(max_length=255, null=True, blank=True)  # Spelling is preserved from source
    mac_address = models.OneToOneField('MacAddress', on_delete=models.SET_NULL, null=True,related_name="home", db_column='mac_address_id')
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    node = models.OneToOneField('Node', on_delete=models.SET_NULL, null=True, db_column='node_id')
    node_switch_unit = models.CharField(max_length=50)
    node_switch_module = models.CharField(max_length=50)
    node_port_num = models.CharField(max_length=50)
    wiring_certified_on = models.DateTimeField(null=True, blank=True)
    wiring_certified_by = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, db_column='wiring_certified_by')
    exclude_from_reports = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "homes"

    def ont(self):
        return Ont.objects.filter(home_id=self.home_id).first()

    def mesh_installs(self):
        return MeshCPEInstall.objects.filter(home_id=self.home_id, deleted_at__isnull=True)

    def subscribers(self):
        return Subscriber.objects.filter(home_id=self.home_id)

    def active_subscriber(self):
        return Subscriber.objects.filter(
            home_id=self.home_id,
            service_activated_on__isnull=False,
            service_deactivated_on__isnull=True
        ).exclude(service_plan_id=1).first()

    def multi_home_subscriber(self):
        return MultiHomeSubscriberHome.objects.filter(home_id=self.home_id).first()

    def uploads(self):
        return Uploads.objects.filter(home_id=self.home_id)

    def alerts(self):
        return HomeAlert.objects.filter(home_id=self.home_id, active=True).order_by('-alert_type_id')

    def port_mac_address(self):
        return PortMacAddress.objects.select_related('mac_address_found').filter(
            node_id=self.node_id,
            node_switch_unit=self.node_switch_unit,
            node_switch_module=self.node_switch_module,
            node_port_num=self.node_port_num
        ).first()
