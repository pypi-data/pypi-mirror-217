# xycu
🍂 An unofficial [*Waifu.pics*](https://waifu.pics) API wrapper for Python

# 📦 Packages
## 🐍 PyPi
```sh
pip install collei
```
# 🔎 Examples
[*examples/basic.py*](https://github.com/elaresai/xycu/blob/main/examples/basic.py)
```py
"""basic.py"""

from collei import Client, SfwCategory

client = Client()

print(client.sfw.get(SfwCategory.HUG))
print(client.sfw.get(SfwCategory.KISS))
print(client.sfw.get(SfwCategory.LICK))
print(client.sfw.get(SfwCategory.BITE))
```

# ✨ Links
[🐍 *PyPi*](https://pypi.org/project/collei/)\
[🏠 *Homepage*](https://github.com/elaresai/collei)\
[🐱 *Repository*](https://github.com/elaresai/collei)
