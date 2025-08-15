import streamlit as st
from utils import df_read, exec_sql, categories
st.title("🧾 Transactions Review")
df = df_read("""select id, ordered_at, merchant_text as merchant, category, amount_aed from txn order by ordered_at desc limit 500""")
if not df.empty:
    edited = st.data_editor(df, num_rows='dynamic', key='txe')
    if st.button("Save edits"):
        ch=0
        for i,row in edited.iterrows():
            orig = df.loc[i]
            if row['category'] != orig['category']:
                exec_sql("update txn set category=%s where id=%s",(row['category'],row['id'])); ch+=1
            if row['merchant'] != orig['merchant']:
                exec_sql("update txn set merchant_text=%s where id=%s",(row['merchant'],row['id'])); ch+=1
        st.success(f"Saved {ch} changes")
else:
    st.info("No transactions yet.")
