import os
from azure.identity import AzureCliCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.recoveryservicesbackup import RecoveryServicesBackupClient
from azure.mgmt.loganalytics import LogAnalyticsManagementClient

# Config
subscription_id = os.popen("az account show --query id -o tsv").read().strip()
credential = AzureCliCredential()

compute_client = ComputeManagementClient(credential, subscription_id)
network_client = NetworkManagementClient(credential, subscription_id)
resource_client = ResourceManagementClient(credential, subscription_id)

def get_vm_details(resource_group, vm_name):
    vm = compute_client.virtual_machines.get(resource_group, vm_name, expand='instanceView')

    # Basic VM Info
    location = vm.location
    size = vm.hardware_profile.vm_size
    os_type = vm.storage_profile.os_disk.os_type.value
    os_disk_size = vm.storage_profile.os_disk.disk_size_gb
    data_disks = vm.storage_profile.data_disks
    data_disk_1_size = data_disks[0].disk_size_gb if data_disks else None
    availability_set = vm.availability_set.id.split('/')[-1] if vm.availability_set else None
    tags = vm.tags

    # NIC & IP
    nic_id = vm.network_profile.network_interfaces[0].id
    nic_rg = nic_id.split("/")[4]
    nic_name = nic_id.split("/")[-1]
    nic = network_client.network_interfaces.get(nic_rg, nic_name)

    private_ip = nic.ip_configurations[0].private_ip_address
    public_ip = None
    app_security_groups = [asg.id.split('/')[-1] for asg in nic.ip_configurations[0].application_security_groups] if nic.ip_configurations[0].application_security_groups else []

    subnet = nic.ip_configurations[0].subnet
    subnet_name = subnet.id.split('/')[-1]
    vnet_name = subnet.id.split('/')[8]
    vnet_rg = subnet.id.split('/')[4]

    # Public IP (if any)
    if nic.ip_configurations[0].public_ip_address:
        public_ip_id = nic.ip_configurations[0].public_ip_address.id
        public_ip_name = public_ip_id.split('/')[-1]
        public_ip = network_client.public_ip_addresses.get(nic_rg, public_ip_name).ip_address

    # VM Extensions
    extensions = compute_client.virtual_machine_extensions.list(resource_group, vm_name)
    extension_names = [ext.name for ext in extensions]

    # Backup info (simplified check using CLI)
    backup_status = os.popen(f"az backup item list --resource-group {resource_group} --vault-name <VAULT_NAME> --query \"[?properties.sourceResourceId=='{vm.id}'].properties.protectionState\" -o tsv").read().strip() or "Not Enabled"

    # Log Analytics (manual check or via CLI)
    log_analytics = os.popen(f"az monitor log-analytics workspace list --resource-group {resource_group} -o table").read().strip()

    # Print Summary
    print(f"\nVM: {vm_name}")
    print(f"Resource Group: {resource_group}")
    print(f"Subscription ID: {subscription_id}")
    print(f"Location: {location}")
    print(f"Size: {size}")
    print(f"Operating System: {os_type}")
    print(f"OS Disk Size (GB): {os_disk_size}")
    print(f"Data Disk-1 Size (GB): {data_disk_1_size}")
    print(f"Availability Set: {availability_set}")
    print(f"Assigned Private IP: {private_ip}")
    print(f"Assigned Public IP: {public_ip}")
    print(f"VNet Name: {vnet_name}")
    print(f"VNet Resource Group: {vnet_rg}")
    print(f"Subnet Name: {subnet_name}")
    print(f"Extensions: {extension_names}")
    print(f"Application Security Groups: {app_security_groups}")
    print(f"Backup Status: {backup_status}")
    print(f"Tags: {tags}")
    print(f"Log Analytics Workspaces:\n{log_analytics}")
    print("-" * 60)

# Example usage
get_vm_details("MyResourceGroup", "MyVM")