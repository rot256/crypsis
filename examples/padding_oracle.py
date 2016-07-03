import requests
from crypsis.cbc.pkcs7 import padding_oracle as oracle

"""
This server is vulnable to a padding oracle attack
Status 403 indicates incorrect padding
"""

msg = 'f20bdba6ff29eed7b046d1df9fb7000058b1ffb4210a580f748b4ac714c001bd4a61044426fb515dad3f21f18aa577c0bdf302936266926ff37dbf7035d5eeb4'.decode('hex')

def query(m):
    resp = requests.get('http://crypto-class.appspot.com/po?er=' + m.encode('hex'))
    return resp.status_code != 403

print 'Plaintext:', oracle.decrypt_msg(msg, query, threads = 4)
