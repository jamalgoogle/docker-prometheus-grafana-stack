مشروع مراقبة باستخدام Prometheus - دليل شامل
📖 نظرة عامة
هذا المشروع يوضح كيفية إعداد نظام مراقبة متكامل باستخدام Prometheus لمراقبة تطبيق ويب وموارد النظام. يتضمن النظام Prometheus لجمع المقاييس، وGrafana لتصور البيانات، وNode Exporter لمراقبة موارد النظام، وتطبيق ويب مخصص يحتوي على مقاييس مدمجة.

🏗️ بنية المشروع
text
prometheus-example/
├── docker-compose.yml      # ملف تكوين Docker لتشغيل جميع الخدمات
├── prometheus.yml          # تكوين خادم Prometheus الرئيسي
├── alert.rules.yml         # قواعد التنبيهات في Prometheus
├── alertmanager.yml        # تكوين إدارة التنبيهات
├── app.py                  # تطبيق الويب مع المقاييس المدمجة
├── requirements.txt        # متطلبات بايثون للتطبيق
└── README.md               # هذا الملف
📁 شرح الملفات ومكوناتها
1. docker-compose.yml
هذا الملف يحتوي على تعريف جميع الخدمات التي سيتم تشغيلها في حاويات Docker.

الخدمات المشمولة:

prometheus: خادم Prometheus الرئيسي لجمع وتخزين المقاييس

alertmanager: نظام إدارة وتوجيه التنبيهات

node-exporter: لجمع مقاييس موارد النظام (CPU، ذاكرة، قرص)

grafana: منصة لتصور البيانات وإنشاء لوحات التحكم

كيفية التشغيل:

bash
# تشغيل الخدمات في الخلفية
docker-compose up -d

# إيقاف الخدمات
docker-compose down

# عرض سجلات الخدمات
docker-compose logs [service-name]
2. prometheus.yml
ملف التكوين الرئيسي لخادم Prometheus يحدد كيفية جمع المقاييس.

الأقسام الرئيسية:

global: الإعدادات العامة (فترات جمع المقاييس)

scrape_configs: قائمة الأهداف التي سيجمع منها Prometheus المقاييس

rule_files: ملفات قواعد التنبيهات

alerting: تكوين إدارة التنبيهات

وظيفة كل job:

prometheus: يراقب خادم Prometheus نفسه

node-exporter: يجمع مقاييس موارد النظام

web-application: يجمع مقاييس تطبيق الويب

3. alert.rules.yml
يحتوي على قواعد التنبيهات التي يتحقق منها Prometheus باستمرار.

القواعد المضمنة:

HighRequestLatency: تنبيه عند تجاوز زمن الاستجابة 0.5 ثانية

ServiceDown: تنبيه عندما يتوقف تطبيق الويب عن الاستجابة

هيكل القاعدة:

alert: اسم التنبيه

expr: تعبير PromQL للتحقق من الشرط

for: المدة التي يجب أن يستمر فيها الشرط قبل تشغيل التنبيه

labels: تسميات إضافية للتنبيه

annotations: معلومات وصفية للتنبيه

4. alertmanager.yml
يتحكم في كيفية معالجة وتوزيع التنبيهات التي يولدها Prometheus.

الميزات الرئيسية:

التجميع: تجميع التنبيهات المتشابهة لتجنب الإشعارات المفرطة

الكبح: منع التنبيهات الزائدة عن الحاجة

التوجيه: إرسال التنبيهات إلى قنوات مختلفة (بريد، Slack، etc.)

المستلمون: تعريف كيفية استلام التنبيهات

5. app.py
تطبيق ويب مبني باستخدام Flask يحتوي على مقاييس مدمجة لـ Prometheus.

المقاييس المضمنة:

http_requests_total: عدد الطلبات HTTP الإجمالي

http_request_latency_seconds: زمن استجابة الطلبات

active_users: عدد المستخدمين النشطين

ال endpoints:

/: الصفحة الرئيسية

/metrics: endpoint للمقاييس (يجمعه Prometheus)

/user/login: محاكاة تسجيل دخول пользователя

/user/logout: محاكاة تسجيل خروج пользователя

6. requirements.txt
قائمة الحزم Python المطلوبة لتشغيل تطبيق الويب.

🚀 خطوات التشغيل الكاملة
1. تثبيت المتطلبات الأساسية
تأكد من تثبيت:

Docker و Docker Compose

Python 3.x

pip (مدير حزم Python)

2. تشغيل حاويات Docker
bash
# انتقل إلى مجلد المشروع
cd prometheus-example

# شغّل جميع الخدمات
docker-compose up -d
3. تشغيل تطبيق الويب
bash
# تثبيت dependencies
pip install -r requirements.txt

# تشغيل التطبيق
python app.py
4. الوصول إلى الخدمات
Prometheus: http://localhost:9090

Grafana: http://localhost:3000 (admin/admin)

تطبيق الويب: http://localhost:8000

Node Exporter: http://localhost:9100

5. إعداد Grafana
سجّل الدخول إلى Grafana (admin/admin)

أضف مصدر بيانات:

انقر على "Add your first data source"

اختر "Prometheus"

في URL أدخل: http://prometheus:9090

انقر على "Save & Test"

أنشئ لوحة تحكم جديدة وأضف panels باستخدام استعلامات PromQL

🔍 استعلامات PromQL مفيدة
promql
# معدل الطلبات في الدقيقة
rate(http_requests_total[1m])

# زمن الاستجابة الحالي
http_request_latency_seconds

# عدد المستخدمين النشطين
active_users

# استخدام الذاكرة
node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes

# استخدام CPU
rate(node_cpu_seconds_total[1m])

# صحة الخدمات
up
🧪 اختبار النظام
اختبر تطبيق الويب بزيارة:

http://localhost:8000

http://localhost:8000/user/login

http://localhost:8000/user/logout

أنشئ حركة مرور باستخدام curl:

bash
while true; do curl http://localhost:8000; sleep 2; done
راقب المقاييس في:

Prometheus: http://localhost:9090/graph

Grafana: http://localhost:3000

🛠 استكشاف الأخطاء وإصلاحها
لم تظهر Targets في Prometheus:

تحقق من أن جميع الحاويات تعمل: docker-compose ps

تحقق من أن تطبيق الويب يعمل: curl http://localhost:8000/metrics

Grafana لا يمكنها الاتصال بـ Prometheus:

تأكد من أن URL هو http://prometheus:9090 وليس http://localhost:9090

لم تظهر المقاييس:

تحقق من أن تطبيق الويب يولد المقاييس: curl http://localhost:8000/metrics

📈 خطوات التطوير المستقبلية
إضافة المزيد من المقاييس للتطبيق

تكوين قنوات إشعارات إضافية في Alertmanager (البريد الإلكتروني، Slack)

إنشاء لوحات تحكم Grafana أكثر تقدمًا

إضافة خدمة قاعدة بيانات ومراقبتها

تكوين اكتشاف تلقائي للخدمات (Service Discovery)

📚 موارد إضافية
توثيق Prometheus الرسمي

توثيق Grafana

Prometheus Client for Python
