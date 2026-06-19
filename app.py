import streamlit as st
from datetime import datetime

st.set_page_config(page_title="AI Trading Bot", layout="centered")

st.title("AI Trading Bot")
st.warning("PAPER TRADING ONLY — no real money connected.")

mode = st.radio(
    "Trading Mode",
    ["Simulation", "Live Armed", "Live Trading"],
    index=0
)

if mode == "Simulation":
    st.success("Simulation mode: fake money only.")

elif mode == "Live Armed":
    st.warning("Live Armed: API can be connected, but trading is still paused.")

elif mode == "Live Trading":
    st.error("LIVE TRADING MODE: Real money risk. Start tiny.")
    confirm = st.checkbox("I understand this can lose real money.")
    if not confirm:
        st.stop()

starting_balance = 1000.00
current_balance = 1000.00
profit_loss = current_balance - starting_balance

st.metric("Paper Balance", f"${current_balance:,.2f}")
st.metric("Profit / Loss", f"${profit_loss:,.2f}")

st.subheader("Bot Controls")

col1, col2 = st.columns(2)

with col1:
    if st.button("Start Bot"):
        st.success("Bot started.")

with col2:
    if st.button("Stop Bot"):
        st.error("Bot stopped.")

st.subheader("Starter Risk Settings")
st.write("Trading pairs: BTC / ETH only")
st.write("Leverage: 1x")
st.write("Max trade size: 2%")
st.write("Daily loss limit: 3%")
st.write("Stop after 2 losses in a row")

st.subheader("Trade Log")
st.write("No trades yet.")
st.caption(f"Last updated: {datetime.now()}")
