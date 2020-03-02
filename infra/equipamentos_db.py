import sqlite3

db_name = "BaseDeDados.db"
table_name = "equipamento"

sql_create_table = f"CREATE TABLE IF NOT EXISTS {table_name} (numeroEquipamento INTEGER PRIMARY KEY AUTOINCREMENT, marca text, modelo text, status TEXT DEFAULT 'ATIVO' CHECK(status IN ('ATIVO','INATIVO')));"

def createTable(cursor, sql):
    cursor.execute(sql)

def popularDb(cursor, numeroEquipamento, marca, modelo, status):
    sql = f"INSERT INTO {table_name} (numeroEquipamento, marca, modelo, status) VALUES (?,?,?,?)"
    cursor.execute(sql, (numeroEquipamento, marca, modelo, status))

def init():
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    createTable(cursor, sql_create_table)
    try:
        popularDb(cursor, 1, 'dell' ,'inspiron15', 'ATIVO')
        popularDb(cursor, 2, 'Motorola' ,'tablet_flip','ATIVO')
        popularDb(cursor, 3, 'Samsung' ,'TB-3500','INATIVO')
    except:
        pass
    cursor.close()
    connection.commit()
    connection.close()
    
init()