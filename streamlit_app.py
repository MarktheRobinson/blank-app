import streamlit as st
import yaml
import pandas as pd
import os
import asyncio
import logging
import traceback
from threading import Thread
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Health check
st.write("App is running...")

try:
    from hummingbot.client.hummingbot_application import HummingbotApplication
    from hummingbot.core.utils.async_utils import safe_ensure_future
    from hummingbot.client.config.config_var import GLOBAL_CONFIG_PATH
except ImportError:
    HummingbotApplication = None
    st.error("Hummingbot module not found. Bot functionality is disabled.")
    logger.error("Hummingbot module not found.")

st.title("Hummingbot Dashboard")

# Load configuration
config_path = "bots/conf/controllers/phoenix-exchange_0.1.yml"
if os.path.exists(config_path):
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    st.write("Configuration loaded successfully:", config)
else:
    st.error(f"Configuration file not found at {config_path}")
    logger.error(f"Configuration file not found: {config_path}")
    st.stop()

# Set up Hummingbot config directory
hummingbot_conf_dir = "/app/conf"
os.makedirs(hummingbot_conf_dir, exist_ok=True)
os.environ["HUMMINGBOT_CONF_DIR"] = hummingbot_conf_dir
logger.info(f"Hummingbot config directory set to: {hummingbot_conf_dir}")

# Patch GLOBAL_CONFIG_PATH
if HummingbotApplication:
    GLOBAL_CONFIG_PATH._value = Path(hummingbot_conf_dir) / "conf_client.yml"
    logger.info(f"Patched GLOBAL_CONFIG_PATH to: {GLOBAL_CONFIG_PATH._value}")

# Ensure conf_client.yml exists
conf_client_path = Path(hummingbot_conf_dir) / "conf_client.yml"
if not conf_client_path.exists():
    try:
        with open(conf_client_path, "w") as f:
            yaml.dump({}, f)
        logger.info(f"Created empty conf_client.yml at {conf_client_path}")
    except Exception as e:
        st.error(f"Failed to create conf_client.yml: {str(e)}")
        logger.error(f"Failed to create conf_client.yml: {str(e)}")

async def initialize_hummingbot(config):
    if HummingbotApplication:
        try:
            logger.info("Initializing Hummingbot...")
            bot = HummingbotApplication()
            # Extract market names from config
            connector = config.get("connector_name", "kraken")
            trading_pair = config.get("trading_pair", "SOLUSDC")
            market_names = {connector: [trading_pair]}
            # Run async initialization tasks
            safe_ensure_future(bot._initialize_notifiers())
            safe_ensure_future(bot._initialize_markets(market_names))
            return bot
        except Exception as e:
            logger.error(f"Error initializing Hummingbot: {str(e)}\n{traceback.format_exc()}")
            raise
    return None

def run_hummingbot():
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        bot = loop.run_until_complete(initialize_hummingbot(config))
        loop.close()
        if bot:
            st.session_state.bot = bot
            st.success("Hummingbot initialized successfully.")
            st.write("Bot Status: Initialized")
            st.write("Exchange:", config.get("exchange", "Not specified"))
            st.write("Trading Pair:", config.get("trading_pair", "Not specified"))
            logger.info("Hummingbot initialized successfully.")
        else:
            st.write("Bot controls are disabled due to missing Hummingbot module.")
            logger.warning("Bot controls disabled due to missing Hummingbot module.")
    except Exception as e:
        st.error(f"Error initializing Hummingbot: {str(e)}")
        st.write("Traceback:", traceback.format_exc())
        logger.error(f"Error initializing Hummingbot: {str(e)}\n{traceback.format_exc()}")

# Initialize Hummingbot
if "bot" not in st.session_state:
    logger.info("Starting Hummingbot initialization...")
    thread = Thread(target=run_hummingbot)
    thread.start()
    thread.join()

if "bot" in st.session_state and st.session_state.bot:
    if st.button("Start Bot"):
        try:
            logger.info("Starting bot...")
            safe_ensure_future(st.session_state.bot.start())
            st.write("Bot started with configuration:", config)
            logger.info("Bot started successfully.")
        except Exception as e:
            st.error(f"Error starting bot: {str(e)}")
            logger.error(f"Error starting bot: {str(e)}")
    if st.button("Stop Bot"):
        try:
            logger.info("Stopping bot...")
            safe_ensure_future(st.session_state.bot.stop())
            st.write("Bot stopped")
            logger.info("Bot stopped successfully.")
        except Exception as e:
            st.error(f"Error stopping bot: {str(e)}")
            logger.error(f"Error stopping bot: {str(e)}")
else:
    st.write("Bot controls are disabled due to initialization failure.")
    logger.warning("Bot controls disabled due to initialization failure.")
