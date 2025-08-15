import streamlit as st
from utils import df_read
import matplotlib.pyplot as plt

st.title("📊 Dashboard")
mtd = df_read("""select category, sum(amount_aed) spent from txn where ordered_at >= date_trunc('month', now()) group by category""")
if not mtd.empty:
    fig, ax = plt.subplots()
    ax.bar(mtd['category'], mtd['spent'])
    st.pyplot(fig)
