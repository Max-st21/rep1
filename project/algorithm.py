import psycopg2
from psycopg2.extensions import register_adapter, AsIs
import numpy as np
import pandas as pd
import re
import json
from datetime import datetime, timedelta
from range_model import weights


def filter_places(df_places, route_param):

    filtered = df_places[
        (df_places["type"].isin(route_param["type"][0]))&
        (df_places["price"] <= route_param["budget"].iloc[0])
        ]

    places=[]
    current_date = datetime.strptime(route_param["day"].iloc[0], "%d.%m.%Y")
    visit_start = datetime.strptime(route_param["start_time"].iloc[0], "%H:%M")
    visit_end = datetime.strptime(route_param["end_time"].iloc[0], "%H:%M")

    for _, place in filtered.iterrows():
        
        weekday=current_date.weekday()
                                
        # Проверяем, что место открыто в это время
        working_hours = place["working_schedule"]
        if (working_hours == ["0:00", "23:59"]):     # если место работает круглосуточно, проверка не проводится
            places.append([place['place_id'],place['average_rating']])
            
        elif ((visit_start >= datetime.strptime(working_hours[str(weekday)][0], "%H:%M"))&
            (visit_end <= datetime.strptime(working_hours[str(weekday)][1], "%H:%M"))):

            places.append([place['place_id'],place['average_rating'],place['type']])

    df_ = pd.DataFrame(places, columns=['place_id','average_rating','type'])
    
    return df_


def rank_places(filtered_places, places_categories,favourite_places,favourite_categories,routes_places,weights):

    filtered_places["score"]=filtered_places["average_rating"] * weights[1]

    for idx, place in filtered_places.iterrows():

        filtered = places_categories[
            (places_categories["place_id"] == place["place_id"])
        ] 

        for ind, place_cat in filtered.iterrows():
            for i, favcat in favourite_categories.iterrows():
                if (favcat["category_id"] == place_cat["category_id"]):
                    filtered_places.at[idx,"score"] += 2*weights[0]
                    
        for i, favplace in favourite_places.iterrows():
            if (place["place_id"] == favplace["place_id"]):
                filtered_places.at[idx,"score"] += 10*weights[2]

        for i in range (0, len(routes_places)):
            if (i == place["place_id"]):
                filtered_places.at[idx,"score"] += 10*weights[3]

    filtered_places = (filtered_places.sort_values(by='score', ascending=False)).reset_index(drop=True)     # сортировка ранжированных мест по рейтингу

    return filtered_places
            

def generate_route(ranked_places,route_param):
    route_places=[]
    types=route_param["type"][0]
    number_places=route_param["number_places"].iloc[0]
    for i in range (0,len(types)):
        rank_places = (ranked_places[ranked_places["type"].isin([types[i]])]).reset_index(drop=True)
        rank_places = rank_places[rank_places.index.isin(range(0,number_places[i]))]
        
        for _, place in rank_places.iterrows():
            route_places.append([route_param['user_id'].iloc[0],place['place_id']])

    return route_places
