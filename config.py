import os
atlas_db_cread={
    'host':os.environ.get("DB_PORT"),
    'user':os.environ.get("DB_USER"),
    'password':os.environ.get("DB_PASSWORD"),
    'port':os.environ.get("DB_PORT")
}

open_search_cread={
    "opensearch_endpoint" :os.environ.get("ELASTIC_SEARCH_HOST"),
    "opensearch_user" : os.environ.get("ELASTIC_SEARCH_USERNAME"),
    "opensearch_password" : os.environ.get("ELASTIC_SEARCH_PASSWORD") 
}

