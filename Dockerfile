FROM hummingbot/hummingbot:latest
WORKDIR /app
COPY . /app
RUN apt-get update && apt-get install -y build-essential && pip install --no-cache-dir --force-reinstall streamlit PyYAML pandas hummingbot==20250525
EXPOSE 8501
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501"]
