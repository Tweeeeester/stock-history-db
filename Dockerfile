## ------------------------------- Builder Stage ------------------------------ ##
FROM python:3.13-bookworm AS builder

RUN apt-get update && apt-get install --no-install-recommends -y build-essential
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Download the latest installer, install it and then remove it
ADD https://astral.sh/uv/install.sh /install.sh
RUN chmod -R 655 /install.sh && /install.sh && rm /install.sh

# Set up the UV environment path correctly
ENV PATH="/root/.local/bin:${PATH}" \
    UV_LINK_MODE=copy

WORKDIR /app

COPY ./pyproject.toml .

RUN uv sync && uv pip install pip


## ------------------------------- Production Stage ------------------------------ ##
FROM python:3.13-bookworm AS production

RUN useradd --create-home appuser
USER appuser

WORKDIR /app

COPY /src src
COPY --from=builder /app/.venv .venv

# Set environment variables for the virtual environment
ENV VIRTUAL_ENV="/app/.venv" \
    PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH=/app/src

# Start the application
CMD ["python", "./src/stock_history_db/main.py"]




