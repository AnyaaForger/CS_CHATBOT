import pypyodbc as odbc
import pandas as pd
import os

DRIVER_NAME = "SQL SERVER"
SERVER_NAME = "DESKTOP-TS9Q2CR"
DATABASE_NAME = "cs_chatbot"

def DataStore(name, number, email, city):
    if os.path.isfile("user_data.xlsx"):
        df = pd.read_excel("user_data.xlsx")
        print(df)
        df = pd.concat([df, pd.DataFrame([[name, number, email, city]],
                          columns = ["name", "number", "email", "city"])], axis=0)
        # df = df.append(pd.DataFrame([[name, number, email, city]],
        #                   columns = ["name", "number", "email", "city"]))
        df.to_excel("user_data.xlsx", index = False)
    else:
        df = pd.DataFrame([[name, number, email, city]],
                          columns = ["name", "number", "email", "city"])
        df.to_excel("user_data.xlsx", index = False)

def DataRead(column, place):
    if os.path.isfile("user_data.xlsx"):
        df = pd.read_excel("user_data.xlsx")
        data = df[column][df["city"] == place]
        return data.to_list()
    else:
        return ["There is no data. "]
    
def DBConnect():
    con_string = f"""
        Driver={{{DRIVER_NAME}}};
        Server={SERVER_NAME};
        Database={DATABASE_NAME};
        Trusted_Connection=True;
        MultipleActiveResultSets=true;
        TrustServerCertificate=True
    """
    
    conn = odbc.connect(con_string)
    print(conn)

    return conn
    
def StoreDataDB(name, number, email, city, table_name):
    conn = DBConnect()
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO {table_name} (name, number, email, city) VALUES (?, ?, ?, ?)", (name, number, email, city))
    conn.commit()
    cursor.close()
    conn.close()

def ReadDataDB(column, place, table_name):
    print("ReadDataDB")
    conn = DBConnect()
    cursor = conn.cursor()
    print(column, place, table_name)
    cursor.execute(f"SELECT {column} FROM {table_name} WHERE city='{place}'")
    rows = cursor.fetchall()
    print(rows)
    data = [row[0] for row in rows]
    cursor.close()
    conn.close()

    return data

def ReadDataMembershipType(membership_type, table_name):
    conn = DBConnect()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name} WHERE name='{membership_type}'")
    rows = cursor.fetchall()
    print(rows)
    data = [value for value in rows[0]]

    print(data)
    cursor.close()
    conn.close()

    return data