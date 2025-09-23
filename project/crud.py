import psycopg2
from psycopg2.extensions import register_adapter, AsIs
from datetime import date
from models import Route, Route_place, User_interests, Route_param
from algorithm import filter_places, rank_places, generate_route
from range_model import weights
import json
import numpy as np
import pandas as pd


def read_routeplaces(cur,route_id):
    places=[]
    places_id=cur.execute("SELECT place_id FROM routes_places WHERE route_id=%s;",(route_id,))
    places_id=cur.fetchall()

    for i in range (0,len(places_id)):
        cur.execute("SELECT place_name FROM places WHERE place_id=%s;",(places_id[i][0],))
        k=cur.fetchall() 
        places.append(k)

    return places


def read_routeparam(cur,route_id):
    route_param=cur.execute("SELECT route_parametrs FROM routes WHERE route_id=%s;",(route_id,))
    route_param=cur.fetchall()

    return route_param


def create_route(cur,conn,route:Route):
    cur.execute("INSERT INTO routes (user_id,route_name,description,creation_date,route_parametrs) VALUES (%s,%s,%s,%s,%s);",
        (route.user_id, route.route_name, route.description,date.today(), json.dumps(route.route_parametrs,ensure_ascii=False)))
    conn.commit()

    return route


def create_routeplaces(cur,conn,route_id):
    df_places = pd.read_sql("SELECT * FROM places", conn)
    route_param=cur.execute("SELECT user_id, route_parametrs FROM routes WHERE route_id=%s;",(route_id,))
    route_param=cur.fetchone()
    user_id=route_param[0]
    route_param=pd.DataFrame(route_param[1])

    places = filter_places(df_places, route_param)

    if not places.empty:
        df_placescat = pd.read_sql("SELECT * FROM places_categories", conn)
        df_favplaces = pd.read_sql("SELECT * FROM favourite_places WHERE user_id=%s", conn, params=(user_id,))
        df_favcat = pd.read_sql("SELECT * FROM favourite_categories WHERE user_id=%s", conn, params=(user_id,))

        routes_id = cur.execute("SELECT route_id FROM routes WHERE user_id=%s;", (user_id,))
        routes_id=cur.fetchall()

        for i in range (0,len(routes_id)):
            df_routeplaces = cur.execute("SELECT place_id FROM routes_places WHERE route_id=%s;",(routes_id[i][0],))
            df_routeplaces=cur.fetchall()
        
        ranked_places=rank_places(places,df_placescat,df_favplaces,df_favcat,df_routeplaces,weights)

        generated_route=generate_route(ranked_places,route_param)
        register_adapter(np.int64, AsIs)
                
        for i in range (0,len(generated_route)):
            rid,plid=generated_route[i][0],generated_route[i][1]
            try:
                cur.execute("INSERT INTO routes_places (route_id,place_id) VALUES (%s, %s);", (rid,plid))
                conn.commit()
            except Error as e:
                conn.rollback()

    return places


def create_interest(cur,conn,user:User_interests):
    for i in range (0,len(user.category_id)):
        cur.execute("INSERT INTO favourite_categories (user_id,category_id) VALUES (%s,%s);",
            (user.user_id, user.category_id[i]))
        conn.commit()

    return user


def create_routeparam(cur,conn,route_id,route_parametrs:Route_param):
    route_dict = route_parametrs.dict()
    cur.execute("UPDATE routes SET route_parametrs=%s WHERE route_id=%s;",
                (json.dumps(route_dict,ensure_ascii=False),route_id))
    conn.commit()

    return route_parametrs


def delete_route(cur,conn,route_id):
    cur.execute("DELETE FROM routes WHERE route_id=%s;",(route_id,))
    conn.commit()

    return route_id


def delete_routeplaces(cur,conn,route_id,route:Route_place):
    for i in range (0,len(route.place_id)):
        cur.execute("DELETE FROM routes_places WHERE route_id=%s AND place_id=%s;",
                    (route_id, route.place_id[i]))
        conn.commit()

    return route



