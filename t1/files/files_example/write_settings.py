f = open("settings.txt", "w")

u = input("name: ")
b = int(input("brightness: "))
v = int(input("volume: "))

text = "{}\n{}\n{}\n".format(b,v,u)
f.write(text)
f.close()
