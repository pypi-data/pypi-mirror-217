# DeepChainMap from the Python documentation

## pip install pydeepchainmap

Useful stuff from the Python documentation: https://docs.python.org/3/library/collections.html#collections.ChainMap

#### Tested against Windows 10 / Python 3.10 / Anaconda 

	
```python
>>> d = DeepChainMap({'zebra': 'black'}, {'elephant': 'blue'}, {'lion': 'yellow'})
>>> d['lion'] = 'orange'         # update an existing key two levels down
>>> d['snake'] = 'red'           # new keys get added to the topmost dict
>>> del d['elephant']            # remove an existing key one level down
>>> d                            # display result
DeepChainMap({'zebra': 'black', 'snake': 'red'}, {}, {'lion': 'orange'})

```