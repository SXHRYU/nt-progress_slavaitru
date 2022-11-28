FROM python:3.11.0-slim-buster
WORKDIR /app
COPY requirements.txt requirements.txt
COPY main.py main.py
COPY commands.py commands.py
COPY exceptions.py exceptions.py
COPY user.py user.py
COPY test_main.py test_main.py
RUN pip install -r requirements.txt

CMD ["/bin/bash", "-c", "pytest -vv .; python3 main.py"]