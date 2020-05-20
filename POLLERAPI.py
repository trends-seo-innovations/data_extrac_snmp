from backend_api.app import app


app.run(host='0.0.0.0',port=os.environ.get("API_PORT"))
