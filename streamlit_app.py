import streamlit as st
import yaml
import os

st.title("Hummingbot Dashboard")

config_path = "bots/conf/controllers/phoenix-exchange_0.1.yml"
if os.path.exists(config_path):
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    st.write("Configuration loaded successfully:", config)
    st.write("Exchange:", config.get("exchange", "Not specified"))
    st.write("Trading Pair:", config.get("trading_pair", "Not specified"))
else:
    st.error(f"Configuration file not found at {config_path}")
