import os

print(os.getcwd())

if os.path.isdir('aaa'):
    print("exist")
else:
    os.mkdir('aaa')
# print(os.geteuid())
print(os.getpid())
# print(os.getuid())