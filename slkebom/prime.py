import json
import sys

prime_file = 'prime.json'
with open(prime_file) as file:
    primes = json.load(file)

if not primes:
    print('Void prime numbers database')
    sys.exit(1)


def is_prime(number):
    for prime in primes:
        if number == prime:
            return True
        if prime > number:
            return False


def three_summand(number):
    smaller_primes = []
    for prime in primes:
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
                    if len(result) == 0:
                        result.append(summands)
                    elif result[0] != summands:
                        result.append(summands)
                        return result
    print('Summands not found')
    return result
