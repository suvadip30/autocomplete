# Introduction

`Dockerfile` to create a [Docker](https://www.docker.com/) container image for [Redis]

Redis is an open source, BSD licensed, advanced key-value cache and store. It is often referred to as a data structure server since keys can contain strings, hashes, lists, sets, sorted sets, bitmaps and hyperloglogs.

## Explanation

- On the execution of the python script app.py will do the autocomplete for the initial letter search.
- Python modules has been used like 
```bash
flask
json
redis
pickle
```
- To store the value in the redis memory the below API will help
```bash
/add_word/word=<path:query
```

- Below API will throwback all the input value as a JSON format
```bash
/autocomplete
```

- This API will again need to give the input as a initial letter of any search.
```bash
/autocomplete/query=<path:query>
```

- The python script has been used to store the value in the json file which will get created if that json file is not present and it will store the value as a key and value in dictionary format.

- That JSON file will be reable and throwback as a json data in the /autocomplete API.

- At the end all the values from the json file will be stored in the redis in - memory with the help of ZADD as a key point name which will be retrieved with the help of ZRANK and ZRANGE with the help of list a byte format.
