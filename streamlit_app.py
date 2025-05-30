import streamlit as st
import yaml
import pandas as pd
import os

try:
    from hummingbot.client.hummingbot_application import HummingbotApplication
except ImportError:
    HummingbotApplication = None
    st.error("Hummingbot module not found. Bot functionality is disabled.")

st.title("Hummingbot Dashboard")

config_path = "bots/conf/controllers/phoenix-exchange_0.1.yml"
if os.path.exists(config_path):
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    st.write("Configuration loaded successfully:", config)
else:
    st.error(f"Configuration file not found at {config_path}")
    st.stop()

if HummingbotApplication:
    try:
        bot = HummingbotApplication()
        st.success("Hummingbot initialized successfully.")
        st.write("Bot Status: Initialized")
        st.write("Exchange:", config.get("exchange", "Not specified"))
        st.write("Trading Pair:", config.get("trading_pair", "Not specified"))
        if st.button("Start Bot"):
            try:
                bot.start()
                st.write("Bot started with configuration:", config)
            except Exception as e:
                st.error(f"Error starting bot: {str(e)}")
        if st.button("Stop Bot"):
            try:
                bot.stop()
                st.write("Bot stopped")
            except Exception as e:
                st.error(f"Error stopping bot: {str(e)}")
    except Exception as e:
        st.error(f"Error initializing Hummingbot: {str(e)}")
else:
    st.write("Bot controls are disabled due to missing Hummingbot module.")
