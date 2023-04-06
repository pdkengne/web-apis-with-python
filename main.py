from typing import List, Optional
from fastapi import FastAPI, Query
from fastapi.encoders import jsonable_encoder
from model.dbHandler import match_exact, match_like

app = FastAPI ()


@app.get("/")
def index():
    """
    DEFAULT ROUTE
    This method will
    1. Provide usage instructions formatted as JSON
    """
    response = { "usage 1" : "/dict?=<word>",
                "usage 2" : "/dicts?words=<word1>&words=<word2>&words=<word3>"}
    return jsonable_encoder( response )


@app.get("/dict")
def dictionary(word : str):
    """
    DEFAULT ROUTE
    This method will
    1. Accept a word from the request
    2. Try to find an exact match, and return it if found
    3. If not found, find all approximate matches and return
    """
    if not word :
        response = { "status" : "error" , "word" : word , "data" : "word not found" }
        return jsonable_encoder( response )
    
    definitions = match_exact( word )
    if definitions :
        response = { "status" : "success" , "word" : word , "data" : definitions }
        return jsonable_encoder( response )
    
    # Try to find an approximate match
    definitions = match_like( word )
    if definitions :
        response = { "status" : "partial" , "word" : word , "data" : definitions }
        return jsonable_encoder( response )
    else :
        response = { "status" : "error" , "word" : word , "data" : "word not found" }
        return jsonable_encoder( response )


@ app.get( "/dicts" )
def dictionaries( words : List[ str ] = Query( None )):
    """
    DICTIONARY ROUTE
    This method will
    1. Accept list of words from the request
    2. Try to find an exact match, and return it if found
    3. If not found, find all approximate matches and return
    """
    
    if not words :
        response = {
        "status" : "error" ,
        "word" : words ,
        "data" : "word not found"
        }
        return jsonable_encoder( response )
    
    # Initialise the response
    response = { "words" : []}
    for word in words :
        # Try to find an exact match
        definitions = match_exact( word )
        if definitions :
            response[ "words" ].append({
            "status" : "success" ,
            "word" : word ,
            "data" : definitions
            })
        else :
            # Try to find an approximate match
            definitions = match_like( word )
            if definitions :
                response[ "words" ].append({
                    "status" : "partial" ,
                    "word" : word ,
                    "data" : definitions
                    })
            else :
                response[ words ].append({
                    "status" : "error" ,
                    "word" : word ,
                    "data" : "word not found"
                    })
        return jsonable_encoder( response )