import sqlite3

#establishing connection between database object and python :

conn = sqlite3.connect('softwareproject.db')

#creating user authentication database (to  match during login and/or store info during signup)
conn.execute('''CREATE TABLE User_Auth(UserId text, Password text not null)''')

#creating user information database (after successfull authentication):

conn.execute('''CREATE TABLE User_Info(UserId text , Password text not null, Reviews text not null, Ratings real)''')

#comitting all the changes :

conn.commit

print('''Database has been generated. Redirect to flask app.py to insert value
           into DB for every instance''')
#database created

#NOTE : RUN ONLY ONCE :
#RUN COUNT : 1
