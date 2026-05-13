FROM python:3.12-slim

# Set environment variables to prevent Python from writing .pyc files and to buffer output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies needed for building certain Python packages
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install uv and project dependencies
# We use --system because we are inside a container and don't need a virtualenv
RUN pip install --no-cache-dir uv
COPY pyproject.toml uv.lock ./
RUN uv pip install --system --no-cache -r pyproject.toml
RUN pip install --no-cache-dir gunicorn

# Copy the rest of your application code
COPY . .

# Create the directory for static files
RUN mkdir -p /app/staticfiles

# Open the port Gunicorn will run on
EXPOSE 8000

# Run migrations, collect static files, and start the server
CMD ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn QuickPay.wsgi:application --bind 0.0.0.0:8000"]