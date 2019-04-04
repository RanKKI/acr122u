# acr122u Python Lib

a python libray of acr122u, support verify key, read and write, also load key to the reader.

## Getting Started

### Prerequisites

 - Have pyscard installed. 

    ```bash
    $ pip install pyscard
    ```
 - Python 3.6 or above
 - acr122u

### Running the code

```
 $ python -i reader.py
 >> sr.read(sector=1)
 ------------------------Sector  1------------------------
 Block  4: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
 Block  5: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
 Block  6: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
 Block  7: 00 00 00 00 00 00 FF 07 80 69 FF FF FF FF FF FF
 ---------------------------------------------------------
```
