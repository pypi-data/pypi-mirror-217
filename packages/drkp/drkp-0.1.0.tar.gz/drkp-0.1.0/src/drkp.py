'''Deterministic RSA Key Pair generator.'''

import base64
import functools
import io
import random

import gmpy2
import paramiko
import rsa

__version__ = '0.1.0'


class Key:
    '''A deterministically generated RSA key pair.'''

    def __init__(self, seed):
        self.p, self.q, self.e, self.d = get(seed)
        self.n = self.p * self.q

    @property
    def public(self):
        def serialize(value):
            if isinstance(value, int):
                buf = []
                while True:
                    buf.insert(0, value & 0xff)
                    value >>= 8
                    if value == 0:
                        break
                if buf[0] & 0x80:
                    buf.insert(0, 0)
                buf = bytes(buf)
            else:
                buf = value
            yield bytes((len(buf) >> b & 0xff for b in (24, 16, 8, 0)))
            yield buf

        with io.BytesIO() as f:
            for x in (b'ssh-rsa', self.e, self.n):
                f.write(b''.join(serialize(x)))
            key = base64.b64encode(f.getvalue())

        return b'ssh-rsa ' + key

    @property
    def private(self):
        return rsa.key.PrivateKey(self.n,
                                  self.e,
                                  self.d,
                                  self.p,
                                  self.q).save_pkcs1('PEM')

    @property
    def pkey(self):
        with io.StringIO(self.private.decode()) as f:
            return paramiko.RSAKey.from_private_key(f)


def gen(seed, nbits=2048, accurate=True, exponent=65537):
    '''generate a deterministic RSA private key'''

    rand = random.Random(seed)

    def getprime(nbits):
        while True:
            x = rand.getrandbits(nbits) | 1
            if gmpy2.is_prime(x) and rsa.prime.is_prime(x):
                return x

    (p, q, e, d) = rsa.key.gen_keys(nbits,
                                    getprime,
                                    accurate=accurate,
                                    exponent=exponent)

    return (p, q, e, d)


@functools.lru_cache
def get(seed, nbits=2048, accurate=True, exponent=65537):
    '''get a deterministic RSA private key'''

    return gen(seed, nbits, accurate, exponent)
