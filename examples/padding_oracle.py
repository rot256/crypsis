import requests
from crypsis.cbc import padding_oracle as oracle
from crypsis.padding.pkcs7 import padding

msg = '''
f20bdba6ff29eed7b046d1df9fb70000
58b1ffb4210a580f748b4ac714c001bd
4a61044426fb515dad3f21f18aa577c0
bdf302936266926ff37dbf7035d5eeb4
'''.replace('\n', '').decode('hex')

def query(m):
    resp = requests.get('http://crypto-class.appspot.com/po?er=' + str(m).encode('hex'))
    return resp.status_code != 403

print 'Plaintext:', str(oracle.decrypt_msg(msg, query, padding, threads=8))
