import os
import sqlite3
from urllib.parse import urlparse

movie_data = [
            {
                "id": 1,
                "title": "Star Wars",
                "director":"George Lucas",
                "year": 1977
            },
            {
                "id": 2,
                "title": "Jaws",
                "year": 1975,
                "director": "Steven Spielberg"
            },
            {
                "id": 3,
                "title": "Jurassic Park",
                "year": 1993,
                "director": "Steven Spielberg"
            }
        ]

def setup(type, path):
    pass
                 
def list():
    
    return [(movie['id'],movie['title'],movie['year'],movie['director']) for movie in movie_data]

def find(id:int):
        
        for movie in movie_data:
            if movie["id"]==id:
                return movie['id'],movie['title'],movie['year'],movie['director']
        return None
    
def insert(title:str, director:str, year:int):

    newid=max([item["id"] for item in movie_data])+1
    movie_data.append({"id":newid,"title":title,"director":director,"year":year})
    return newid

def update(id:int, title:str, director:str, year:int):

    rows=0    
    for movie in movie_data:
        if movie["id"]==id:
            movie["title"]=title
            movie["director"]=director
            movie["year"]=year
            rows+=1
            break
    return rows

def delete( id:int):
    
    for i in range(len(movie_data)):
        if movie_data[i]["id"]==id:
            del movie_data[i]
            break