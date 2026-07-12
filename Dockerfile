FROM public.ecr.aws/lambda/python:3.12

# Instala o Poetry
RUN pip install poetry

WORKDIR ${LAMBDA_TASK_ROOT}

# Copia os arquivos do Poetry
COPY pyproject.toml poetry.lock* ./

# Instala apenas as dependências (sem instalar o projeto)
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --only main

# Copia o código da aplicação
COPY src ./src

# Handler da Lambda
CMD ["src.extract.lambda_extract.lambda_handler"]