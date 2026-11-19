#!/usr/bin/env python
"""Script para criar superuser automaticamente"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pesquisador_project.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('✓ Superuser criado com sucesso!')
    print('  Username: admin')
    print('  Password: admin123')
else:
    print('✓ Superuser "admin" já existe')
