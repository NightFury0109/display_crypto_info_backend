pip install fastapi
pip install "uvicorn[standard]"
uvicorn messari:app --reload
Visit Link example: 
Function 1: http://127.0.0.1:8000/f1?before=2022-03-16&limit=01&name=btc
Function 2: http://127.0.0.1:8000/f2?name=btc
Function 3: http://127.0.0.1:8000/f3?name=btc