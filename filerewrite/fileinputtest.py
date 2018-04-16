import fileinput

with fileinput.input(files=('data.txt'), inplace=True) as file:
    for line in file:
        line = line.replace('test', 'testY')
        print(line, end='')
