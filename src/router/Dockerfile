FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install redis pydantic
CMD ["python", "tmr_router.py"]
