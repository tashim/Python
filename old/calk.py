
def Calck(arg=''):
    Var = {}
    arg = "a = "+arg
    try:
        exec ( arg, globals(),Var )
        ret = Var["a"]
    except Exception as e:
        ret = e
    return ret
while True:
    text = input(">>>>> ")
    res = Calck(text)
    if isinstance(res,int):
        print(res)
    else:
        print("Error:",res)