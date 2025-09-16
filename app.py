from flask import Flask, request
from prometheus_client import Counter, Gauge, generate_latest, REGISTRY
import time
import random

app = Flask(__name__)

# تعريف المقاييس
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP Requests',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Gauge(
    'http_request_latency_seconds',
    'HTTP Request Latency',
    ['method', 'endpoint']
)

ACTIVE_USERS = Gauge(
    'active_users',
    'Number of active users'
)

@app.route('/')
def home():
    start_time = time.time()
    
    # محاكاة معالجة الطلب مع تأخير عشوائي
    delay = random.uniform(0.1, 1.0)
    time.sleep(delay)
    
    # تسجيل المقياس
    REQUEST_COUNT.labels(
        method='GET',
        endpoint='/',
        status='200'
    ).inc()
    
    latency = time.time() - start_time
    REQUEST_LATENCY.labels(
        method='GET',
        endpoint='/'
    ).set(latency)
    
    return 'مرحباً بك في التطبيق! زمن التحميل: {:.2f} ثانية'.format(latency)

@app.route('/metrics')
def metrics():
    return generate_latest(REGISTRY)

@app.route('/user/login')
def user_login():
    ACTIVE_USERS.inc()
    return 'تم تسجيل الدخول - المستخدمين النشطين: {}'.format(ACTIVE_USERS._value.get())

@app.route('/user/logout')
def user_logout():
    if ACTIVE_USERS._value.get() > 0:
        ACTIVE_USERS.dec()
    return 'تم تسجيل الخروج - المستخدمين النشطين: {}'.format(ACTIVE_USERS._value.get())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)