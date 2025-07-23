from django.db import models

class PortMacAddress(models.Model):
    PortMacAddress_id = models.AutoField(primary_key=True)
    node = models.ForeignKey('Node', on_delete=models.SET_NULL, null=True, blank=True, db_column='node_Id', related_name='port_mac_addresses')
    node_switch_unit = models.IntegerField(null=True, blank=True)
    node_switch_module = models.IntegerField(null=True, blank=True)
    mac_address = models.CharField(max_length=255)
    node_port_vlanid = models.IntegerField(null=True, blank=True)
    node_oper_status = models.CharField(max_length=255, null=True, blank=True)
    node_admin_status = models.CharField(max_length=255, null=True, blank=True)
    node_rate_up = models.IntegerField(null=True, blank=True)
    node_rate_down = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'port_mac_address'

    def __str__(self):
        return f"MAC {self.mac_address} @ Node {self.node_id}"

    @property
    def mac_address_found(self):
        from .mac_address import MacAddress
        return MacAddress.objects.filter(address=self.mac_address).first()

    @property
    def home_found(self):
        from .home import Home
        return Home.objects.filter(
            node_id=self.node_id,
            node_switch_unit=self.node_switch_unit,
            node_switch_module=self.node_switch_module,
            node_port_num=getattr(self, 'node_port_num', None)  # optional field, see note below
        ).select_related('mac_address').first()
