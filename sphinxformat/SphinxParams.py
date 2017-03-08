# Copyright 2011 Ian Goldberg
#
# This file is part of Sphinx.
#
# Sphinx is free software: you can redistribute it and/or modify
# it under the terms of version 3 of the GNU Lesser General Public
# License as published by the Free Software Foundation.
#
# Sphinx is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with Sphinx.  If not, see
# <http://www.gnu.org/licenses/>.
#
# The LIONESS implementation and the xcounter CTR mode class are adapted
# from "Experimental implementation of the sphinx cryptographic mix
# packet format by George Danezis".

import os
from bearandlion import lioness
from curve25519 import keys
from SphinxNymserver import Nymserver

try:
    from Crypto.Cipher import AES
    from Crypto.Hash import SHA256, HMAC
    from Crypto.Util import number, strxor
except:
    print "\n\n*** You need to install the Python Cryptography Toolkit. ***\n\n"
    raise

try:
    from curvedh import *
except:
    pass

class Group_ECC:
    "Group operations in ECC"

    def __init__(self):

        self.g = b'\x00'*31+b'\x09'

    def gensecret(self):
        key = keys.Private()
        return key.private

    def expon(self, base, exp):
        key = keys.Private(secret=exp)
        return key.get_shared_key(keys.Public(base), hashfunc=lambda x: x)

    def multiexpon(self, base, exps):
        baseandexps = [base]
        baseandexps.extend(exps)
        return reduce(self.expon, baseandexps)

    def makeexp(self, data):
        assert len(data) == 32
        key = keys.Private(secret=data)
        return key.private

    def in_group(self, alpha):
        # All strings of length 32 are in the group, says DJB
        return len(alpha) == 32

    def printable(self, alpha):
        return alpha.encode("hex")

class SphinxParams:
    k = 16 # in bytes, == 128 bits
    m = 1024 # size of message body, in bytes
    pki = {} # mapping of node id to node
    clients = {} # mapping of destinations to clients

    def __init__(self, r=5):
        self.r = r
        self.group = Group_ECC()
        self.nymserver = Nymserver(self)

    def xor(self, str1, str2):
        # XOR two strings
        assert len(str1) == len(str2)
        return strxor.strxor(str1,str2)

    class xcounter:
        # Implements a string counter to do AES-CTR mode
        i = 0
        def __init__(self, size):
            self.size = size

        def __call__(self):
            ii = number.long_to_bytes(self.i)
            ii = '\x00' * (self.size-len(ii)) + ii
            self.i += 1
            return ii

    # The PRG; key is of length k, output is of length (2r+3)k
    def rho(self, key):
        assert len(key) == self.k
        c = AES.new(key, AES.MODE_CTR, counter=self.xcounter(self.k))
        return c.encrypt("\x00" * ( (2 * self.r + 3) * self.k ))

    # The HMAC; key is of length k, output is of length k
    def mu(self, key, data):
        m = HMAC.new(key, msg=data, digestmod=SHA256)
        return m.digest()[:self.k]

    # The PRP; key is of length k, data is of length m
    def pi(self, key, data):
        assert len(key) == self.k
        assert len(data) == self.m

        return lioness.encrypt(key, data)

    # The inverse PRP; key is of length k, data is of length m
    def pii(self, key, data):
        assert len(key) == self.k
        assert len(data) == self.m

        return lioness.decrypt(key, data)

    # The various hashes

    def hash(self, data):
        h = SHA256.new()
        h.update(data)
        return h.digest()

    def hb(self, alpha, s):
        "Compute a hash of alpha and s to use as a blinding factor"
        group = self.group
        return group.makeexp(self.hash("hb:" + group.printable(alpha)
            + " , " + group.printable(s)))

    def hrho(self, s):
        "Compute a hash of s to use as a key for the PRG rho"
        group = self.group
        return (self.hash("hrho:" + group.printable(s)))[:self.k]

    def hmu(self, s):
        "Compute a hash of s to use as a key for the HMAC mu"
        group = self.group
        return (self.hash("hmu:" + group.printable(s)))[:self.k]

    def hpi(self, s):
        "Compute a hash of s to use as a key for the PRP pi"
        group = self.group
        return (self.hash("hpi:" + group.printable(s)))[:self.k]

    def htau(self, s):
        "Compute a hash of s to use to see if we've seen s before"
        group = self.group
        return (self.hash("htau:" + group.printable(s)))

if __name__ == '__main__':
    p = SphinxParams(5, True)
    print p.hb(p.group.g, p.group.g).encode("hex")
    print p.rho("1234" * 4).encode("hex")
