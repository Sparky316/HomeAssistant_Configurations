To Install this custom component, simply follow these instructions:
1.) Copy the “lutron_qse” folder to the HA server as follows:
	..\config\custom_components\lutron_qse

2.)	Then restart!

3.)	Add the following code to ..\config\configuration.yaml

# NOTE: This first Section is optional.  It will display info about what devices that lutron_qse discovers.
# You can look through this list of devices to determine the serial numbers of any device(s) that you might want to ignore/disable.

logger:
  default: warning
  logs:
    custom_components.lutron_qse: info

# Configure lutron_qse.  This is a "QS Standalone" Lutron system "QSE-CI-NWK-E", often used for shades.
#  The only required parameter is the host IP address.  Optionally, you can indicate devices to ignore.
lutron_qse:
    host: 192.168.0.123
#    ignore:
#      - '0x00da1ba2'
#      - '0x00daffff'


4.)	Then restart again!
