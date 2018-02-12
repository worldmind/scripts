import configparser
import prime

cfg = configparser.ConfigParser()
cfg.read('config.ini')
cfg = cfg['analyzer']


def analyze(number):
    result = dict()
    result['number'] = number
    if prime.is_prime(number):
        result['prime'] = True
    else:
        result['prime'] = False
    if number > int(cfg['find_summand_from']):
        res = prime.three_summand(number)
        result['option_1'] = res[0]
        result['option_2'] = res[1]
    return result
