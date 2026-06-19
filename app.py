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
