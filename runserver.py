import uvicorn
from src.config import environment

if __name__ == '__main__':

    reload = True if environment.get_item(
        key='ENVIRONMENT', default='production') == 'development' else False
    debug = environment.get_item(key='DEBUG', default=False)
    host = environment.get_item(key='HOST', default='0.0.0.0')
    port = int(environment.get_item(key='PORT', default=5000))
    uvicorn.run("application:app", host="0.0.0.0", port=port,
                reload=reload, debug=debug)
