FROM python:3.10-slim

WORKDIR /code/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /code/

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /code/requirements.txt

COPY . /code/

EXPOSE 8000

CMD ["alembic", "upgrade head", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--reload"]