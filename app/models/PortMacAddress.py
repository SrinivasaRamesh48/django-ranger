from django.db import models
from django.core.exceptions import ObjectDoesNotExist # For handling lookups

# Import related models
from .Node import Node # Ensure Node model is defined
from .MacAddress import MacAddress # Ensure MacAddress model is defined


class PortMacAddress(models.Model):
    id = models.AutoField(primary_key=True) # Laravel's primaryKey is 'id'

    # Foreign Key to Node
    # Note: Laravel uses 'node_Id' (capital 'I') in fillable, but 'node_id' in relationship.
    # We use 'node' as the Django field name and 'db_column' to match your actual column.
    node = models.ForeignKey(
        Node,
        on_delete=models.CASCADE, # Assuming if a node is deleted, its port MAC addresses are too
        db_column='node_Id', # Match original Laravel column name if it's 'node_Id'
        related_name='port_mac_addresses'
    )
    node_switch_unit = models.IntegerField()
    node_switch_module = models.IntegerField()
    # Note: 'mac_address' field in this model also acts as a lookup key for 'mac_address_found'
    mac_address = models.CharField(max_length=17, blank=True, null=True) # Standard MAC address length (e.g., AA:BB:CC:DD:EE:FF)

    # Other fields from fillable
    created_at = models.DateTimeField(auto_now_add=True)
    # The Laravel fillable doesn't include updated_at, but Django adds it by default
    updated_at = models.DateTimeField(auto_now=True) # Assuming this column exists in DB or you want it managed by Django

    node_port_vlanid = models.CharField(max_length=255, blank=True, null=True) # Assuming VLAN ID is string
    node_oper_status = models.CharField(max_length=50, blank=True, null=True) # Operational Status (e.g., 'up', 'down')
    node_admin_status = models.CharField(max_length=50, blank=True, null=True) # Administrative Status (e.g., 'up', 'down')
    node_rate_up = models.IntegerField(blank=True, null=True) # Assuming integer for rate (e.g., Mbps)
    node_rate_down = models.IntegerField(blank=True, null=True) # Assuming integer for rate (e.g., Mbps)

    class Meta:
        db_table = 'port_mac_address'
        app_label = 'app'
        # Optional: Add a unique constraint if a specific port only has one MAC address entry
        unique_together = ('node', 'node_switch_unit', 'node_switch_module', 'mac_address') # Example unique constraint

    def __str__(self):
        return f"Port {self.node_switch_unit}/{self.node_switch_module} MAC: {self.mac_address} on Node {self.node_id}"

    # Custom methods/properties for Laravel's dynamic relations
    # ---------------------------------------------------------

    @property
    def mac_address_found(self):
        # Equivalent of Laravel's `hasOne('App\MacAddress', 'address', 'mac_address')`
        # This implies that `MacAddress.address` is a unique field you're linking against.
        try:
            return MacAddress.objects.get(address=self.mac_address)
        except MacAddress.DoesNotExist:
            return None
        except Exception as e:
            # Handle other potential errors during lookup
            print(f"Error fetching mac_address_found for {self.mac_address}: {e}")
            return None


    @property
    def home_found_info(self): # Renamed to avoid potential conflict if 'home_found' becomes a model field
        # Equivalent of Laravel's `Home::with(['mac_address'])->where([...])->first()`
        # This requires `node_port_num` to be available on `PortMacAddress`
        # (It was not in your Laravel fillable for PortMacAddress, but implied by Laravel query)
        # If `node_port_num` exists on PortMacAddress's table:
        if not hasattr(self, 'node_port_num') or self.node_port_num is None:
             # If node_port_num is not a direct field on PortMacAddress
             # you might need to fetch it from the related Node or reconsider the lookup logic.
             # For now, assuming it exists on PortMacAddress based on Laravel query context.
             pass # Will raise error if node_port_num is not a field here

        try:
            # Assuming Home model has 'node_id', 'node_switch_unit', 'node_switch_module', 'node_port_num'
            # and 'mac_address' relationship
            from .Home import Home
            home = Home.objects.select_related('mac_address').filter(
                node_id=self.node_id,
                node_switch_unit=self.node_switch_unit,
                node_switch_module=self.node_switch_module,
                node_port_num=self.node_port_num
            ).first()
            return home
        except ObjectDoesNotExist:
            return None
        except Exception as e:
            print(f"Error fetching home_found_info: {e}")
            return None