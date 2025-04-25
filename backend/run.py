import os
import sys

# --- Жёсткий патч autoreload для PyInstaller ---
import django.utils.autoreload

def noop(*args, **kwargs):
    return []

django.utils.autoreload.get_child_arguments = noop
django.utils.autoreload.restart_with_reloader = lambda *a, **kw: None
# ------------------------------------------------

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')  # замените на путь к вашим настройкам

import django
from django.core.management.commands.runserver import Command as runserver

django.setup()

cmd = runserver()
cmd.stdout = sys.stdout
cmd.stderr = sys.stderr
# Передаем use_ipv6 явно, чтобы избежать KeyError
cmd.handle(addrport='127.0.0.1:8000', use_reloader=False, use_threading=False, use_ipv6=False, skip_checks=False)

# Если захотите добавить задержку для просмотра ошибок:
# input("Нажмите Enter для выхода...")
