FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements_streamlit.txt /app/requirements_streamlit.txt
RUN pip install --no-cache-dir -r /app/requirements_streamlit.txt

# Copy the Streamlit app
COPY streamlit_frontend.py /app/streamlit_frontend.py

# Expose port for Streamlit
EXPOSE 8501

# Run Streamlit
CMD ["streamlit", "run", "streamlit_frontend.py", "--server.address", "0.0.0.0", "--server.port", "8501"]