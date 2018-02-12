import configparser
import number_analyzer

cfg = configparser.ConfigParser()
cfg.read('config.ini')
cfg = cfg['analyzer']


def test_summands_founded():
    for number in range(int(cfg['min_number']), int(cfg['max_number'])+1):
        result = number_analyzer.analyze(number)
        if number > int(cfg['find_summand_from']) and not result['prime']:
            assert 'option_1' in result and sum(result['option_1']) == number
            assert 'option_2' in result and sum(result['option_2']) == number
