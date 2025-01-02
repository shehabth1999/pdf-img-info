#!/bin/bash

# Run the tests with pytest
pytest --disable-warnings

# After tests, run the Django server
python manage.py runserver 0.0.0.0:8000
