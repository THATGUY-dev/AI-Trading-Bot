import streamlit as st
import pandas as pd
import random
from datetime import datetime

st.set_page_config(page_title="AI Trading Bot", layout="centered")

st.title("AI Trading Bot")
st.warning("SIMULATION ONLY — no real money connected.")

if "balance" not in st.session_state:
    st.session_state.balance = 1000.00
if "position" not in st.session_state:
    st.session_state.position = None
if "trades" not in st.session_state:
    st.session_state.trades = []

mode = st.radio("Trading Mode", ["Simulation", "Live Armed", "Live Trading"], index=0)

if mode != "Simulation":
    st.error("Live trading is locked for now. We are testing simulation first.")
    st.stop()

st.subheader("Account")
st.metric("Paper Balance", f"${st.session_state.balance:,.2f}")

st.subheader("Bot Controls")

col1, col2, col3 = st.columns(3)

with col1:
    start = st.button("Run One Scan")

with col2:
    close = st.button("Close Position")

with col3:
    reset = st.button("Reset Bot")

if reset:
    st.session_state.balance = 1000.00
    st.session_state.position = None
    st.session_state.trades = []
    st.success("Bot reset.")

price = random.choice([62500, 62800, 63100, 63500, 64000, 64500])
signal = random.choice(["BUY", "SELL", "WAIT"])

st.subheader("Market Scan")
st.write(f"BTC Price Checked: ${price:,.2f}")
st.write(f"Bot Signal: **{signal}**")

if start:
    if st.session_state.position is None:
        if signal == "BUY":
            trade_size = st.session_state.balance * 0.02
            st.session_state.position = {
                "pair": "BTC/USD",
                "side": "LONG",
                "entry": price,
                "size": trade_size,
                "time": datetime.now().strftime("%m/%d/%Y %I:%M %p")
            }
            st.success("Opened simulated LONG position.")
        else:
            st.info("Bot decided not to enter a trade.")
    else:
        st.info("Bot already has an open position.")

if close and st.session_state.position is not None:
    entry = st.session_state.position["entry"]
    size = st.session_state.position["size"]

    percent_move = (price - entry) / entry
    pnl = size * percent_move
    st.session_state.balance += pnl

    trade_record = {
        "Pair": st.session_state.position["pair"],
        "Side": st.session_state.position["side"],
        "Entry": entry,
        "Exit": price,
        "Size": round(size, 2),
        "P/L": round(pnl, 2),
        "Opened": st.session_state.position["time"],
        "Closed": datetime.now().strftime("%m/%d/%Y %I:%M %p")
    }

    st.session_state.trades.append(trade_record)
    st.session_state.position = None

    if pnl >= 0:
        st.success(f"Closed position for profit: ${pnl:.2f}")
    else:
        st.error(f"Closed position for loss: ${pnl:.2f}")

elif close and st.session_state.position is None:
    st.info("No open position to close.")

st.subheader("Open Position")

if st.session_state.position:
    pos = st.session_state.position
    current_pnl = pos["size"] * ((price - pos["entry"]) / pos["entry"])

    st.write(f"Pair: **{pos['pair']}**")
    st.write(f"Side: **{pos['side']}**")
    st.write(f"Entry Price: **${pos['entry']:,.2f}**")
    st.write(f"Current Price: **${price:,.2f}**")
    st.write(f"Position Size: **${pos['size']:,.2f}**")
    st.write(f"Unrealized P/L: **${current_pnl:.2f}**")
else:
    st.write("No open position.")

st.subheader("Trade History")

if st.session_state.trades:
    df = pd.DataFrame(st.session_state.trades)
    st.dataframe(df)
else:
    st.write("No completed trades yet.")

st.subheader("Risk Settings")
st.write("Trading pair: BTC only")
st.write("Mode: Simulation")
st.write("Trade size: 2% of paper balance")
st.write("No leverage")
st.write("Only one open trade at a time")
