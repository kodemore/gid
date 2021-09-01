# Gid
Gid is a small library for generating short globally unique, sortable uri safe identifiers.

## Features
- Generated ids are sortable
- Generated ids carry creation time expressed in microseconds
- Generated ids are globally unique
- Minimal footprint
- High performance


## Installation

With pip,
```shell
pip install gid
```
or through poetry
```shell
poetry add gid
```

# Usage

## Generating id
```python
from gid import Guid

some_id = Guid()
some_id.timestamp # contains timestamp expressed in milliseconds
str(some_id) # can be cast to a string
```

## Recreating id from string
```python
from gid import Guid
my_id = Guid()

same_id = Guid(str(my_id))

assert same_id == my_id
assert same_id.timestamp == my_id.timestamp
```

# Id structure
Generated identifiers are case-sensitive, which means string functions (like lowercase or uppercase) on generated 
identifiers may break it because `Sbt5LrD9iSAwb300` is not the same value as `Sbt5LrD9iSAwB300`.

The below diagram represents single identifier's structure, which is 16-character long:
```
    Sbt5LrD9iSAwb300
    |      |      |
    +- first 7 characters for millisecond timestamp
           |      |
           +- next 7 characters is randomly generated hash
                  |
                  + last two characters to ensure uniqueness of guid in a single millisecond
```

> Within 1 ms there can be 62^2 unique generated ids on a single machine.
