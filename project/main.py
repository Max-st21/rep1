from fastapi import FastAPI, HTTPException
from db import postgresql_pool, get_conn
from psycopg2 import Error, pool
from crud import (read_routeplaces, read_routeparam, create_route,
    create_routeplaces, create_interest, create_routeparam,
    delete_route, delete_routeplaces)
from models import Route, Route_place, User_interests, Route_param
import json

#uvicorn project.main:app --reload

app = FastAPI()


@app.get("/routes/{route_id}/places")
def read_routesplaces(route_id:int):
    try:
        cur,conn=get_conn(postgresql_pool)
        
        places = read_routeplaces(cur,route_id)

        return places

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        postgresql_pool.putconn(conn)

    
@app.get("/routes/{route_id}/params")
def read_routesparam(route_id:int):
    try:
        cur,conn=get_conn(postgresql_pool)

        route_param = read_routeparam(cur,route_id)

        return route_param

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        postgresql_pool.putconn(conn)

    
@app.get("/routes/create/{route_id}")
def create_routesplaces(route_id: int):
    try:
        cur,conn=get_conn(postgresql_pool)

        places = create_routeplaces(cur,conn,route_id)

        if places.empty:
            raise HTTPException(status_code=404,
                detail=str(e))
        
        return places

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        postgresql_pool.putconn(conn)


@app.post("/routes/create")
def create_routes(route:Route):
    try:
        cur,conn=get_conn(postgresql_pool)
        
        route = create_route(cur,conn,route)
        
        return route

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        postgresql_pool.putconn(conn)


@app.post("/interests/create")
def create_interests(user:User_interests):
    try:
        cur,conn=get_conn(postgresql_pool)
        
        interests = create_interest(cur,conn,user)
        
        return interests

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        postgresql_pool.putconn(conn)


@app.put("/routes/create/param")
def create_routesparam(route_id:int,route:Route_param):
    try:
        cur,conn=get_conn(postgresql_pool)
        
        route_param = create_routeparam(cur,conn,route_id,route)
        
        return route_param

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        postgresql_pool.putconn(conn)

    
@app.delete("/routes/delete/{route_id}")
def delete_routes(route_id:int):
    try:
        cur,conn=get_conn(postgresql_pool)
        
        deleted_route = delete_route(cur,conn,route_id)
        
        return deleted_route

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        postgresql_pool.putconn(conn)


@app.delete("/routes/delete/{route_id}/places")
def delete_routesplaces(route_id:int,route:Route_place):
    try:
        cur,conn=get_conn(postgresql_pool)
        
        deleted = delete_routeplaces(cur,conn,route_id,route)
        
        return deleted

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        postgresql_pool.putconn(conn)
