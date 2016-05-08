# Crypsis
A cryptoanalytical framework in python2

Crypsis is focused on practical attacks against cryptografic systems and being useful in Capture The Flag tournaments. The interface aims to be as simple as possible while still relatively flexible, below an example of a padding oracle attack:

```python
import requests
from crypsis.cbc.pkcs7 import padding_oracle as oracle

msg = 'f20bdba6ff29eed7b046d1df9fb7000058b1ffb4210a580f748b4ac714c001bd4a61044426fb515dad3f21f18aa577c0bdf302936266926ff37dbf7035d5eeb4'.decode('hex')

def query(m):
	p = m.encode('hex')
    resp = requests.get('http://crypto-class.appspot.com/po?er=' + p)
    return resp.status_code != 403

print 'Plaintext:', oracle.decrypt_msg(msg, query, threads = 4)
```

This project is under active development, if you have any new attacks (or old CTF scripts) you wish to add you are more than welcome to contribute.
