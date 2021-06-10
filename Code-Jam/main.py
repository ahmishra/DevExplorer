from MySQLdb import *
##Image
with open('name.jpg','rb') as get:
    with open ('new.jpg','wb') as set:
        set.write(get.read())
