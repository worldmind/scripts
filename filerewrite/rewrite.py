import filerewrite

filename = 'data.txt'
with open(filename, 'r+') as file:
    data = file.read()
    data = data.replace('test', 'testX')
    filerewrite.rewrite(file, data)
