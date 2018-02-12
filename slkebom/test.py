#!/usr/bin/python3

import sys
import time
import number_analyzer

if len(sys.argv) < 2:
    print('Give me integer as argument')
    sys.exit(1)

start_time = time.process_time()
result = number_analyzer.analyze(int(sys.argv[1]))
elapsed_time = time.process_time() - start_time
print(result)
print("Time used: ", elapsed_time)
