import streamlit as st
import yaml
import pandas as pd
import os
import asyncio
from threading import Thread

try:
    from hummingbot.client.hummingbot_application import HummingbotApplication
except ImportError:
    HummingbotApplication = None
    st.error("Hummingbot module not found. Bot functionality is disabled.")

st.title("Hummingbot Dashboard")

# Load configuration
config_path = "bots/conf/controllers/phoenix-exchange_0.1.yml"
if os.path.exists(config_path):
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    st.write("Configuration loaded successfully:", config)
else:
    st.error(f"Configuration file not found at {config_path}")
    st.stop()

# Set up Hummingbot config directory
hummingbot_conf_dir = "/app/conf"
os.makedirs(hummingbot_conf_dir, exist_ok=True)
os.environ["HUMMINGBOT_CONF_DIR"] = hummingbot_conf_dir

def run_hummingbot():
    if HummingbotApplication:
        try:
            bot = HummingbotApplication()
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            st.session_state.bot = bot
            st.success("Hummingbot initialized successfully.")
            st.write("Bot Status: Initialized")
            st.write("Exchange:", config.get("exchange", "Not specified"))
            st.write("Trading Pair:", config.get("trading_pair", "Not specified"))
        except Exception as e:
            st.error(f"Error initializing Hummingbot: {str(e)}")
    else:
        st.write("Bot controls are disabled due to missing Hummingbot module.")

# Initialize Hummingbot in a separate thread
if "bot" not in st.session_state:
    thread = Thread(target=run_hummingbot)
    thread.start()
    thread.join()

if "bot" in st.session_state and st.session_state.bot:
    if st.button("Start Bot"):
        try:
            st.session_state.bot.start()
            st.write("Bot started with configuration:", config)
        except Exception as e:
            st.error(f"Error starting bot: {str(e)}")
    if st.button("Stop Bot"):
        try:
            st.session_state.bot.stop()
            st.write("Bot stopped")
        except Exception as e:
            st.error(f"Error stopping bot: {str(e)}")
else:
    st.write("Bot controls are disabled due to initialization failure.")
