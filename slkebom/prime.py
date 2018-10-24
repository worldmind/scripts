import json
import sys

PRIME_FILE = 'prime.json'
with open(PRIME_FILE) as file:
    PRIMES = json.load(file)

if not PRIMES:
    print('Void prime numbers database')
    sys.exit(1)


def is_prime(number):
    for prime in PRIMES:
        if number == prime:
            return True
        if prime > number:  # optimization
            return False
    return False


def three_summand(number):
    smaller_primes = []
    for prime in PRIMES:
        if prime <= number:
            smaller_primes.append(prime)
    result = []
    for first in reversed(smaller_primes):
        for second in smaller_primes:
            if first + second >= number:
                continue
            for third in smaller_primes:
                if number == first + second + third:
                    summands = sorted([first, second, third])
                    if not result:
                        result.append(summands)
                    elif result[0] != summands:
                        result.append(summands)
                        return result
    print('Summands not found')
    return result
