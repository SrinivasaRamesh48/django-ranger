from django.db import models
from app.models.mac_address import MacAddress

class PortMacAddress(models.Model):
    id = models.AutoField(primary_key=True)
    node = models.ForeignKey('Node', on_delete=models.CASCADE, db_column='node_Id')
    node_switch_unit = models.IntegerField()
    node_switch_module = models.IntegerField()
    mac_address = models.CharField(max_length=17)
    node_port_vlanid = models.IntegerField(blank=True, null=True)
    node_oper_status = models.CharField(max_length=50, blank=True, null=True)
    node_admin_status = models.CharField(max_length=50, blank=True, null=True)
    node_rate_up = models.CharField(max_length=50, blank=True, null=True)
    node_rate_down = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = "port_mac_address"
    

    @property
    def mac_address_found(self):
        try:
            return MacAddress.objects.get(address=self.mac_address)
        except MacAddress.DoesNotExist:
            return None

    @property
    def home_found(self):
        from .home import Home
        try:
            return Home.objects.get(
                node_id=self.node_Id,
                node_switch_unit=self.node_switch_unit,
                node_switch_module=self.node_switch_module,
                # Assuming node_port_num is the field to match against
                # This might need adjustment based on the actual schema
                # node_port_num=self.node_port_num
            )
        except Home.DoesNotExist:
            return None