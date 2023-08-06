# A set that handles all kinds of objects (hashable or not) and preserves the order of the elements

## pip install screwhashesset

#### Tested against Windows 10 / Python 3.10 / Anaconda 

	
```python

from screwhashesset import ScrewHashesSet

s1 = ScrewHashesSet([[(43, 5), 1, 2], 3, {3, 4, 5, 6}, {2: 3, 3: 5}, {2: 3, 3: 6}])
s2 = ScrewHashesSet([(2, 3), [1, 2], 3, 4, {3, 4, 5}, {2: 3, 3: 5}, {1: 32}])
print(s1 - s2)
print(s2 - s1)
print(s2 | s1)
print(s2 & s1)

# str():  {[(43, 5), 1, 2], {3, 4, 5, 6}, {2: 3, 3: 6}}
# repr(): ScrewHashesSet([[(43, 5), 1, 2], {3, 4, 5, 6}, {2: 3, 3: 6}])

# str():  {(2, 3), [1, 2], 4, {3, 4, 5}, {1: 32}}
# repr(): ScrewHashesSet([(2, 3), [1, 2], 4, {3, 4, 5}, {1: 32}])

# str():  {(2, 3), [1, 2], 3, 4, {3, 4, 5}, {2: 3, 3: 5}, {1: 32}, [(43, 5), 1, 2], {3, 4, 5, 6}, {2: 3, 3: 6}}
# repr(): ScrewHashesSet([(2, 3), [1, 2], 3, 4, {3, 4, 5}, {2: 3, 3: 5}, {1: 32}, [(43, 5), 1, 2], {3, 4, 5, 6}, {2: 3, 3: 6}])

# str():  {3, {2: 3, 3: 5}}
# repr(): ScrewHashesSet([3, {2: 3, 3: 5}])
```