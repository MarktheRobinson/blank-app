import streamlit as st
import yaml
import os
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

st.write("App is running...")
st.title("Hummingbot Dashboard")

try:
    import hummingbot
    st.write("Hummingbot module found:", hummingbot.__version__)
except ImportError as e:
    st.error(f"Failed to import hummingbot: {str(e)}")
    logger.error(f"Failed to import hummingbot: {str(e)}")
    st.stop()

config_path = "bots/conf/controllers/phoenix-exchange_0.1.yml"
if os.path.exists(config_path):
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    st.write("Configuration loaded successfully:", config)
else:
    st.error(f"Configuration file not found at {config_path}")
    logger.error(f"Configuration file not found: {config_path}")
