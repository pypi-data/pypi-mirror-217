# python-yapi
Python Client for [YApi](https://github.com/YMFE/yapi) based on HTTP Api.


![Languate - Python](https://img.shields.io/badge/language-python-blue.svg)
![PyPI - License](https://img.shields.io/pypi/l/python-yapi)
![PyPI](https://img.shields.io/pypi/v/python-yapi)
![PyPI - Downloads](https://img.shields.io/pypi/dm/python-yapi)

## Install
```shell
pip install python-yapi
```

## Simple Use

### Register and Login
```python
from python_yapi import YApi
yapi = YApi(base_url='http://localhost:3000')

username, email, password = 'Kevin', 'kevin@126.com', 'abc123'

yapi.register(username, email, password)  # return a dict
yapi.login( email, password) # return a dict
```


### Mange Projects

```python
from python_yapi import YApi
yapi = YApi(base_url='http://localhost:3000')
email, password = 'kevin@126.com', 'abc123'
yapi.login(email, password)

# Create a private project in user default group, with auto basepath, random color and random icon.
yapi.add_project('Demo Project')

```
