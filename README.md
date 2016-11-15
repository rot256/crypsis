# Crypsis

A Crypto CTF framework for python2.
I found myself often rewriting the same code over and over for CTFs, hence crypsis.
The goal is to be a little like [Pwntools](https://github.com/Gallopsled/pwntools)
by with a focus on crypto challenges (as oppose to binary reversing/exploit).

The library aims to contain useful helper functions and even some full attacks,
below an example of a padding oracle attack:

```python
import requests
from crypsis.cbc.pkcs7 import padding_oracle as oracle

msg = '''
f20bdba6ff29eed7b046d1df9fb7000058b1
ffb4210a580f748b4ac714c001bd4a610444
26fb515dad3f21f18aa577c0bdf302936266
926ff37dbf7035d5eeb4'''.replace('\n', '').decode('hex')

def query(m):
    resp = requests.get('http://crypto-class.appspot.com/po?er=' + m.encode('hex'))
    return resp.status_code != 403

print 'Plaintext:', oracle.decrypt_msg(msg, query, threads = 4)
```

This project is under active development, if you have any new attacks (or old CTF scripts) 
you wish to add you are more than welcome to contribute.
