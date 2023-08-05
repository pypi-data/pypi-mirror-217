# xycu
An unofficial Python [waifu.pics](https://waifu.pics) API wrapper

![language](https://img.shields.io/badge/language-Python-009933)
![license](https://img.shields.io/badge/license-MIT-cafffe)

# Installation
`pip install xycu`

# Examples
`examples/basic.py`
```py
"""basic.py"""

from xycu import Client, SfwCategory

client = Client()

print(client.sfw.get(SfwCategory.HUG).url)
print(client.sfw.get(SfwCategory.KISS).url)
print(client.sfw.get(SfwCategory.LICK).url)
print(client.sfw.get(SfwCategory.BITE).url)
```

# Links
[🐍 **PyPi**](https://pypi.org/project/xycu/)\
[🏠 **Homepage**](https://github.com/elaresai/xycu)\
[🐱 **Repository**](https://github.com/elaresai/xycu)
