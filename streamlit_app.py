import streamlit as st
import yaml
from hummingbot.client.hummingbot_application import HummingbotApplication
import pandas as pd
import os

st.title("Hummingbot Dashboard")

# Check if config file exists
config_path = "bots/conf/controllers/phoenix-exchange_0.1.yml"
if os.path.exists(config_path):
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    st.write("Configuration loaded successfully:", config)
else:
    st.error(f"Configuration file not found at {config_path}")
    st.stop()

# Initialize Hummingbot
try:
    bot = HummingbotApplication()
    st.success("Hummingbot initialized successfully.")
    
    # Display basic bot status
    st.write("Bot Status: Initialized")
    st.write("Exchange:", config.get("exchange", "Not specified"))
    st.write("Trading Pair:", config.get("trading_pair", "Not specified"))
    
    # Placeholder for bot controls
    if st.button("Start Bot"):
        st.write("Bot start functionality not yet implemented.")
    if st.button("Stop Bot"):
        st.write("Bot stop functionality not yet implemented.")
except Exception as e:
    st.error(f"Error initializing Hummingbot: {str(e)}")
