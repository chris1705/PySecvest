# PySecvest
Python module to access status information provided by ABUS Secvest alarm system by using non-official REST API.

The current version was just written 'quick and dirty', so it does only provide read-only features. Please do not use it in production unless you know what you're doing.

## Compatibility
I have tested PySecvest with the current Abus Secvest (FUAA50000) with the firmware verion v.1.00.00. May be it is also compatible with other versions, but I can't test it. Please let me know, if you used it with Secvest 2WAY or Secvest IP sucessfully.

## Example usage
```python

from secvest import Secvest
secvest = Secvest(hostname="192.168.178.2", username="Administrator", password="123456")

# Get system info
print secvest.get_system()

# Get a list of partitions
print secvest.get_partitions()

# Get info about partition 1
print secvest.get_partition(1)

# Logout from secvest
secvest.logout()

```