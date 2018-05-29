# Shavtsak


Tired of creating your own Shavtsak? wished for more automation while keeping the flexibility and control?

Introducing **Shavtsak**:

Shavtsak is a powerful tool for generating schedules for the army troops.

  - Add information about each soldier
  - Create schedule template
  - Magic

## Getting Started:
### Install:
###### pip
```console
$ pip install shavtsak-cli
```
###### manual install
```console
$ git clone https://github.com/jelomite/Shavtsak-CLI.git
$ cd Shavtsak-CLI
$ python setup.py install
```


### Usage
#### Example usage:
```python
from shavtsak import Shavtsak, Soldier

adam = Soldier('Adam', 2)
noy = Soldier('Noy', 2)
gil = Soldier('Gil', 0)
s = Shavtsak([adam, noy, gil])

s.assign(gil, 'sunday', 'kitchen')
s.fill()

print(s)
```
For full documentation, please continue reading.

---

## API

### Shavtsak(soldiers: list)
creates a new shavtsak that contains all the soldiers that it should assign

type: Object

### Soldier(name: str, pazam: int)
creates a new soldier. the pazam indicates the number of iterations that are in the platoon. The youngest iteration of a trooper must be 0.

---

### Help Needed
It all sounds too perfect, which is why this isn't even close to a its final product.
If you're a programmer that wishes to help, I'll be more than grateful.
