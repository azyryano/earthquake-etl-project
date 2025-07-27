FROM public.ecr.aws/lambda/python:3.11

RUN yum install -y \
    gcc \
    gcc-c++ \
    python3-devel \
    postgresql-devel \
    libffi-devel \
    openssl-devel \
    make \
    wget

WORKDIR /app

# ✅ Pin numpy and pandas versions to avoid GCC 9+ issues
RUN pip install --upgrade pip && \
    pip install "numpy<1.26" "pandas<2.1.0" "psycopg2-binary==2.9.9" -t /app

COPY lambda_function.py .

CMD ["lambda_function.lambda_handler"]
