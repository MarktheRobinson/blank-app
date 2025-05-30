FROM hummingbot/hummingbot:latest
WORKDIR /app
COPY . /app
RUN pip install streamlit PyYAML pandas hummingbot==20250525
EXPOSE 8501
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501"]
