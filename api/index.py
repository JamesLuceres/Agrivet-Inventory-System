import os
import sys
from pathlib import Path

# Add backend folder to sys.path
root_dir = Path(__file__).resolve().parent.parent
backend_dir = root_dir / 'backend'

if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

from django.core.wsgi import get_wsgi_application

app = get_wsgi_application()
