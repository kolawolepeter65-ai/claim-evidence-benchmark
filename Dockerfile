FROM python:3.12-slim
WORKDIR /workspace
COPY pyproject.toml ./
COPY src/ src/
COPY tests/ tests/
COPY data/ data/
RUN python -m pip install --no-cache-dir -e '.[test]'
CMD ["python", "-m", "pytest", "-q"]
