from gmpy2 import next_prime, is_prime
from random import choice
from os import urandom

from threading import Lock

from crypsis import logger, csprng
from crypsis.encode import bit_size
from crypsis.exceptions import essert, NoSolution

### Lazy list of primes ###

class PrimeCache:
    def __init__(self, INIT_BOUND=2**18):
        """
        Caches a list of small primes
        """
        self.cache = [2]
        self.bound = 2
        self.lock = Lock()
        self.init = INIT_BOUND

    def expand_with(self, n):
        """
        Expands the cache with n new primes
        """
        self.lock.acquire()
        while n > 0:
            self.bound = next_prime(self.bound)
            self.cache.append(self.bound)
            n -= 1
        self.lock.release()

    def expand_to(self, n):
        """
        Expand the prime cache to all primes <= n
        """
        if n <= self.bound:
            return
        self.lock.acquire()
        while self.bound <= n:
            self.bound = next_prime(self.bound)
            self.cache.append(self.bound)
        self.lock.release()

    def get_some(self, n):
        """
        Get all primes in the cache to <= n
        """
        self.expand_to(self.init)
        self.lock.acquire()
        bot = 0
        top = len(self.cache)
        while 1:
            if top - bot <= 1:
                break
            test = (top + bot) // 2
            if self.cache[test] > n:
                top = test
                continue
            bot = test
        primes = self.cache[:top]
        self.lock.release()
        return primes

    def get_all(self, n):
        """
        Get all primes <= n
        and add these to the cache
        """
        self.expand_to(n)
        return self.get_some(n)

primecache = PrimeCache()

### Primes generation ###

def random(bitlen, min_len=None):
    if min_len == None:
        min_len = bitlen
    mask = 1 << (bitlen - 1) | 1
    while 1:
        can = csprng.getrandbits(bitlen) | mask
        if is_prime(can):
            return can
        if bit_size(can) < min_len:
            continue

def safe(bitlen):
    """
    Generate a safe prime of bitlen bits
    """
    mask = 1 | (1 << (bitlen - 2))
    while 1:
        can = csprng.getrandbits(bitlen - 2) | mask
        if not is_prime(can):
            continue
        p = can * 2 + 1
        if not is_prime(p):
            continue
        if bit_size(p) == bitlen:
            return p

def range(min_val, max_val=1<<16):
    if max_val < min_val:
        max_val = min_val * 2
    while 1:
        can = csprng.randrange(min_val, max_val)
        if is_prime(can):
            return can

def smooth(min_val, max_val=None, b=2**16, exclude=set([]), unique=False):
    """
    Generates a prime p where p-1 is b smooth
    (not the prime itself -- which would be pretty useless)

    :param min_val: Minimal value of the prime
    :param max_val: Maximum value of the prime
    :b: Smoothness of p-1
    :excludes: List of prime factors to exclude
    :unique: Should all prime factors of p-1 be unique?
    :return: A prime number p with p-1 begin b-smooth 
             and a list of prime factors (for p-1)

    TODO: Fix this doc string (use google format)
    """

    # Acquire a list of small primes
    essert(max_val is None or max_val > min_val, NoSolution)
    essert(2 not in exclude, NoSolution)
    primes = primecache.get_some(b)
    primes = filter(lambda x: x not in exclude, primes)
    
    while 1:
        # Generate random smooth number
        n = 2
        f = {2: 1}
        while n <= min_val:
            p = choice(primes)
            if p in f:
                if unique:
                    continue
                f[p] += 1
            else:
                f[p] = 1
            n *= p

        # Check if prime
        if not is_prime(n + 1):
            continue
        if max_val is None:
            break
        if n + 1 <= max_val:
            break

    # Expand dict into list
    facs = []
    for k, v in f.items():
        facs += [int(k)] * v
    return int(n + 1), sorted(facs)

### Prime factors ###

from primefac import primefac

def factors(num):
    """
    Decomposes a number into a list of its prime factors
    
    Args:
        num (int): An integer to factor

    Returns:
        list: A list of prime factors
    """
    return map(lambda x: int(x), primefac(num))
