import configparser
import prime

CFG = configparser.ConfigParser()
CFG.read('config.ini')
CFG = CFG['analyzer']


def analyze(number):
    result = dict()
    result['number'] = number
    result['prime'] = prime.is_prime(number)
    if number > int(CFG['find_summand_from']):
        res = prime.three_summand(number)
        result['option_1'] = res[0]
        result['option_2'] = res[1]
    return result
