import sqlite3

db_name = "BaseDeDados.db"
table_name = "usuarios"

sql_create_table = f"CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY AUTOINCREMENT, numeroMatricula INTEGER, departamento text, email text );"

def createTable(cursor, sql):
    cursor.execute(sql)

def popularDb(cursor, id, numeroMatricula, departamento, email):
    sql = f"INSERT INTO {table_name} (id, numeroMatricula, departamento, email) VALUES (?,?,?,?)"
    cursor.execute(sql, (id, numeroMatricula, departamento, email))

def init():
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    createTable(cursor, sql_create_table)
    try:
        popularDb(cursor, 1, 111,'professor1', 'professor1@professor1.com.br')
        popularDb(cursor, 2, 222 ,'professor2', 'professor2@professor2.com.br')
        popularDb(cursor, 3, 333 ,'professor3', 'professor3@professor3.com.br')
        
    except:
        pass
    cursor.close()
    connection.commit()
    connection.close()
    
init()