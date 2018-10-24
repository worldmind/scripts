import configparser
import number_analyzer

CFG = configparser.ConfigParser()
CFG.read('config.ini')
CFG = CFG['analyzer']


def test_summands_founded():
    for number in range(int(CFG['min_number']), int(CFG['max_number'])+1):
        result = number_analyzer.analyze(number)
        if number > int(CFG['find_summand_from']) and not result['prime']:
            assert 'option_1' in result and sum(result['option_1']) == number
            assert 'option_2' in result and sum(result['option_2']) == number
