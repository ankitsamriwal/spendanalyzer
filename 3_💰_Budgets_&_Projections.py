import streamlit as st
from datetime import date
from utils import df_read, exec_sql, categories
st.title("💰 Budgets & Projections")
month = date.today().replace(day=1)
vals = {}
cols = st.columns(4)
for i,c in enumerate(categories()):
    vals[c]= cols[i%4].number_input(f"{c} (AED)", min_value=0.0, step=50.0)
if st.button("Save budgets"):
    uid = df_read("select id from app_user order by created_at limit 1").iloc[0,0]
    for c,v in vals.items():
        exec_sql("""insert into budget(user_id,month,category,limit_aed) values (%s,%s,%s,%s)
        on conflict (user_id,month,category) do update set limit_aed=excluded.limit_aed""", (uid, str(month), c, float(v)))
    st.success("Budgets saved.")
