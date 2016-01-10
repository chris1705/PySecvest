# PySecvest
Python module to access status information provided by ABUS Secvest alarm system.

The current version was just wirtten 'quick and dirty', so it does only provide read-only features. Please do not use it in production unless you know what you're doing.

# Compatibility
Probably the module is only compatible with the current version of the Abus Secvest (FUAA50000) 

# Example usage
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
