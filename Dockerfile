# Dockerfile
## -----------------------------------------------------
FROM dhi.io/python:3.13-alpine3.23-dev AS build-stage

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/librotea/program/venv/bin:$PATH"

WORKDIR /librotea

COPY requirements.txt .
RUN python -m venv /librotea/program/venv
RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir -p /librotea/AudioBooks && mkdir -p /librotea/working_dir && chown -R 1000 /librotea

## -----------------------------------------------------
FROM dhi.io/python:3.13-alpine AS runtime-stage

WORKDIR /librotea
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/librotea/program/venv/bin:$PATH"

COPY --from=build-stage --chown=1000:1000 /librotea /librotea

COPY --chown=1000:1000 --chmod=+x utils /librotea/program/utils
COPY --chown=1000:1000 --chmod=+x librotea.py __init__.py /librotea/program/
COPY --chown=1000:1000 --chmod=+x docker/libro-tea-loop.py /librotea/libro-tea-loop.py
COPY --chown=1000:1000 docker/config.json.example docker/account.json.example /librotea/example/

USER 1000:1000

ENV LIBRO_TEA_export_cue=False

# Set Libro Tea dir

ENV LIBRO_TEA_account_dir=/librotea/config
ENV LIBRO_TEA_config_dir=/librotea/config
ENV LIBRO_TEA_database_dir=/librotea/config
ENV LIBRO_TEA_output_dir=/librotea/AudioBooks
ENV LIBRO_TEA_working_dir=/librotea/working_dir

# Set Libro Tea autorun rate

ENV LIBRO_TEA_second=0
ENV LIBRO_TEA_min=30
ENV LIBRO_TEA_hour=0
ENV LIBRO_TEA_day=0

CMD ["python", "/librotea/libro-tea-loop.py"]