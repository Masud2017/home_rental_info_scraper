import psycopg2
from psycopg2.extras import RealDictCursor
from secrets import  DB
from models.Home import Home

def query_db(query: str, params: list[str] = [], fetchOne: bool = False) -> list[dict] | dict | None:
    db = psycopg2.connect(database=DB["database"],
                            host=DB["host"],
                            user=DB["user"],
                            password=DB["password"],
                            port=DB["port"])
    
    cursor = db.cursor(cursor_factory=RealDictCursor)
    cursor.execute(query, params)
    
    # Try, because not all queries will return data
    try:
        if fetchOne:
            result = cursor.fetchone()
        else:
            result = cursor.fetchall()
    except:
        result = None
    
    db.commit()
    cursor.close()
    db.close()
    
    return result
