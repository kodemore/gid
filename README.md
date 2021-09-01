# Gid <br> [![Release](https://github.com/kodemore/gid/actions/workflows/release.yml/badge.svg)](https://github.com/kodemore/gid/actions/workflows/release.yml) [![Linting and Tests](https://github.com/kodemore/gid/actions/workflows/main.yaml/badge.svg)](https://github.com/kodemore/gid/actions/workflows/main.yaml) [![codecov](https://codecov.io/gh/kodemore/gid/branch/main/graph/badge.svg?token=N6AROCAN9S)](https://codecov.io/gh/kodemore/gid) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
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

## Example ids

```
ShmX2HaaUB9UQL02 
ShmX2JGvSk4ZyZ13 
ShmX2Ku8mDizRc23 
ShmX2MWQVL5J7022 
ShmX2OCegs4MdP22 
ShmX2Pu2MDVFHa02 
ShmX2RYngGET4Z32 
ShmX2TCM6v701q23 
ShmX2UrBjxNGYM11
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

> Within 1 ms there can be (62^2 - 620) unique generated ids on a single machine.
