from dbMan import *
file = open('removes-28.1.csv','r')
wfile = open('rem_Bmby.csv','w')
wfile2 = open('rem_noBmby.csv','w')
db = connnect()
text = ' '
count =0
while 1:
    text= file.readline()
    if text == '' : break
    count +=1
    # print(text.split(',')[0])
    cur = db.cursor()
    cur.execute("SELECT b_entryID,FirstName,LastName,Phone1,Phone2,Email FROM Individual where Phone1 ='"+ text.split(',')[0]+"' or Phone2 ='"+ text.split(',')[0]+"';")
    for x in cur.fetchall():
        # print(x)
        if len(x) > 0:
            if x[0] >2:
                # print('BMBY  ',x[-1])
                for i in x:
                    wfile.write(str(i)+',')
                wfile.write('\n')
            else:
                for i in x:
                    wfile2.write(str(i)+',')
                wfile2.write('\n')
   # cur = db.cursor()
   #  cur.execute("UPDATE  Individual set Activities=201 where Phone1 like '%"+ text.split(',')[0]+"' or Phone2 like '%"+ text.split(',')[0]+"';")
   #  db.commit()

file.close()
wfile.close()
wfile2.close()
print(count)