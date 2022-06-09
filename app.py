import textwrap
import pyodbc
import os
from flask import Flask, request, redirect, url_for, render_template


############################
### PYODBC CONNECTIVITY ####
############################

#specify the driver
driver = '{ODBC Driver 13 for SQL Server}'

#specify the server name and database name
server_name = 'assignment01'
database_name = 'assignment01'

#create server URL
server = '{server_name}.database.windows.net,1433'.format(server_name=server_name)

#define username and Password
username = 'supreetha'
password = 'Chuppi$123'

#create full connection string
connection_string = textwrap.dedent(''' 
    Driver={driver};
    Server={server};
    Database={database};
    Uid={username};
    Pwd={password};
    Encrypt=yes;
    TrustServerCertificate=no;
    Connection Timeout=30;
'''.format(
    driver=driver,
    server=server,
    database=database_name,
    username=username,
    password=password
))

#create a new PYODBC connection object
cnxn: pyodbc.Connection = pyodbc.connect(connection_string)

#create a cursor object from the connection
crsr: pyodbc.Cursor = cnxn.cursor()


app = Flask(__name__)

#for home page to be displayed
@app.route('/')
def home():
    return render_template('index.html')

# 1st Query
@app.route('/form', methods=['GET','POST'])
def form():
    getname1 = str(request.args.get('fname1')) 
    getname2 = str(request.args.get('fname2'))
    select_sql = "select Name, Keywords, Picture from data where Height between '"+getname1+"' and '"+getname2+"' ;"
    crsr.execute(select_sql)
    result = crsr.fetchall()
    print(result)   
    return render_template('form.html', setimage=result)
    cnxn.close()

@app.route('/display', methods=['GET','POST'])
def dis():
    select_sql = "select Name, Picture from data;"
    crsr.execute(select_sql)
    result2 = crsr.fetchall()
    print(result2)   
    return render_template('display.html', setimage=result2)
    cnxn.close()

if __name__ == "__main__":
    app.run()
