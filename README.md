Here’s a markdown version of your Bash script setup, explaining each step in a structured way:

```markdown
# Django Project Setup with REST API and Real-Time Functionality

This guide outlines the steps to set up a Django project with a REST API and WebSocket support using Django Channels.

## Prerequisites

Ensure you have the following installed:
- Python 3
- pip
- Virtual environment tools

---

## Step 1: Update System and Install Necessary Packages

```bash
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-venv
```

---

## Step 2: Create and Activate a Virtual Environment

```bash
python3 -m venv aenzbi_env
source aenzbi_env/bin/activate
```

---

## Step 3: Install Django and Related Dependencies

```bash
pip install django djangorestframework channels
```

---

## Step 4: Initialize Django Project and Application

```bash
django-admin startproject aenzbi_project
cd aenzbi_project
django-admin startapp accounting
```

---

## Step 5: Update Project Settings

Add the following to `aenzbi_project/settings.py`:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'accounting',
    'channels',
]

ASGI_APPLICATION = 'aenzbi_project.asgi.application'
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}
```

---

## Step 6: Define Models

Add the following to `accounting/models.py`:

```python
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()

class Transaction(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.DateTimeField(auto_now_add=True)
```

---

## Step 7: Create Serializers

Add the following to `accounting/serializers.py`:

```python
from rest_framework import serializers
from .models import Product, Transaction

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
```

---

## Step 8: Create API Views

Add the following to `accounting/views.py`:

```python
from rest_framework import viewsets
from .models import Product, Transaction
from .serializers import ProductSerializer, TransactionSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
```

---

## Step 9: Add API Routing

Create `accounting/urls.py`:

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, TransactionViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'transactions', TransactionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
```

Include it in `aenzbi_project/urls.py`:

```python
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('accounting.urls')),
]
```

---

## Step 10: Set Up Django Channels

Create `aenzbi_project/asgi.py`:

```python
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
import accounting.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aenzbi_project.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                accounting.routing.websocket_urlpatterns
            )
        )
    ),
})
```

Create `accounting/routing.py`:

```python
from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/sync/', consumers.SyncConsumer.as_asgi()),
]
```

Create a simple consumer in `accounting/consumers.py`:

```python
import json
from channels.generic.websocket import WebsocketConsumer

class SyncConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def receive(self, text_data):
        data = json.loads(text_data)
        # Handle incoming data and update models
        self.send(text_data=json.dumps({
            'message': 'Data received'
        }))
```

---

## Step 11: Migrate Database and Create Superuser

```bash
python manage.py migrate
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'password')" | python manage.py shell
```

---

## Step 12: Run the Development Server

```bash
python manage.py runserver
```

---

## Final Notes

- Access the admin panel at `http://127.0.0.1:8000/admin/` using the credentials:  
  - Username: `admin`  
  - Password: `password`
- API endpoints are available at `http://127.0.0.1:8000/api/`.
- WebSocket endpoint is available at `ws://127.0.0.1:8000/ws/sync/`.

```
