from flask import Flask, render_template
import redis
import os

app = Flask(__name__)  # Убрали явное указание template_folder

# Подключение к Redis
redis_host = os.environ.get('REDIS_HOST', 'redis')
redis_port = int(os.environ.get('REDIS_PORT', 6379))

redis_client = redis.Redis(
    host=redis_host,
    port=redis_port,
    db=0,
    decode_responses=True
)

@app.route('/')
def index():
    try:
        visits = redis_client.incr('page_visits')
        redis_info = {
            'host': redis_host,
            'port': redis_port,
            'connected': redis_client.ping()
        }
    except redis.ConnectionError as e:
        visits = 'Error: Cannot connect to Redis'
        redis_info = {'error': str(e)}
    
    return render_template('index.html', 
                         visits=visits, 
                         redis_info=redis_info)

@app.route('/health')
def health():
    try:
        redis_client.ping()
        return {'status': 'healthy', 'redis': 'connected'}, 200
    except:
        return {'status': 'unhealthy', 'redis': 'disconnected'}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)