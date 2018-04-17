import in_place

with in_place.InPlace('data.txt') as file:
    for line in file:
        line = line.replace('test', 'testZ')
        file.write(line)
