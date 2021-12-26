f = open('settings.txt')

lines = f.readlines()

brightness = int(lines[0])
volume = int(lines[1])
username = lines[2].strip()

print('''
brightness = {}
volume = {}
username = {}
'''.format(brightness, volume, username))

f.close()





















