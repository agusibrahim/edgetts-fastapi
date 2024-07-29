# Gunakan image dasar dari FastAPI
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

# Atur direktori kerja di dalam container
WORKDIR /app

# Salin requirements.txt ke direktori kerja
COPY ./app/requirements.txt /app/requirements.txt

# Instal dependensi dari requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Salin semua file dari direktori lokal ke direktori kerja di dalam container
COPY ./app /app

# Jalankan server Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

