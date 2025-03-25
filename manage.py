#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mma_gym.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()

from cours.models import CategorieCours, Cours

categorie = CategorieCours.objects.create(nom='MMA')

cours = Cours.objects.create(
    titre='Initiation MMA', 
    categorie=categorie, 
    description='Cours pour débutants', 
    niveau='debutant', 
    duree=60, 
    prix=50.00
)