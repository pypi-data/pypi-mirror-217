# dnac_device_list

dnac_device_list is a Python library that makes your life easier when you want to programatically find out 
the location name and location id of any given device that is managed Cisco DNA Center.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install dnac_device_list.

```bash
pip install dnac_device_list
```

## Usage

```python
from dnac_device_list import device_list

# initializes class
dnac = device_list.Dnac(base_url="https://dnac.gma.ciscolabs.com", token=token, verify=False)

# returns 'list of devices'
device_list = dnac.get_device_list_with_location()


```

## Contributing

Pull requests are welcome. For major changes, please reach out to author via email first.
to discuss what you would like to change.
https://github.com/alekos3/DNAC_Device_Location


## License

[MIT](https://choosealicense.com/licenses/mit/)

## Authors
Alexios Nersessian
email: anersess@cisco.com