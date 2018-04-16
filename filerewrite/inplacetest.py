import in_place

with in_place.InPlace('data.txt') as file:
    data = file.read()
    data = data.replace('test', 'testZ')
    file.write(data)
