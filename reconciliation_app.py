import streamlit as st
import pandas as pd

st.title("📊 Transaction Reconciliation Tool")

st.write("Upload your **Bank CSV** and **Ledger CSV** to automatically reconcile transactions.")

# Upload files
bank_file = st.file_uploader("Upload Bank Transactions CSV", type="csv")
ledger_file = st.file_uploader("Upload Ledger CSV", type="csv")

if bank_file and ledger_file:
    # Read CSVs
    bank = pd.read_csv(bank_file)
    ledger = pd.read_csv(ledger_file)

    # Optional: Clean data (strip spaces, standardize date format)
    bank['Date'] = pd.to_datetime(bank['Date'])
    ledger['Date'] = pd.to_datetime(ledger['Date'])

    bank['Description'] = bank['Description'].str.strip()
    ledger['Description'] = ledger['Description'].str.strip()

    # Match transactions on Date + Amount
    matched = pd.merge(bank, ledger, on=['Date','Amount'], how='inner', suffixes=('_bank','_ledger'))

    # Unmatched transactions
    unmatched_bank = bank.merge(matched[['Date','Amount']], on=['Date','Amount'], how='left', indicator=True)
    unmatched_bank = unmatched_bank[unmatched_bank['_merge'] == 'left_only'].drop(columns=['_merge'])

    unmatched_ledger = ledger.merge(matched[['Date','Amount']], on=['Date','Amount'], how='left', indicator=True)
    unmatched_ledger = unmatched_ledger[unmatched_ledger['_merge'] == 'left_only'].drop(columns=['_merge'])

    # Display results
    st.subheader("✅ Matched Transactions")
    st.dataframe(matched)

    st.subheader("❌ Unmatched Bank Transactions")
    st.dataframe(unmatched_bank)

    st.subheader("❌ Unmatched Ledger Transactions")
    st.dataframe(unmatched_ledger)

    # Download buttons
    st.download_button(
        label="Download Matched Transactions CSV",
        data=matched.to_csv(index=False).encode('utf-8'),
        file_name='matched_transactions.csv',
        mime='text/csv'
    )
    st.download_button(
        label="Download Unmatched Bank CSV",
        data=unmatched_bank.to_csv(index=False).encode('utf-8'),
        file_name='unmatched_bank.csv',
        mime='text/csv'
    )
    st.download_button(
        label="Download Unmatched Ledger CSV",
        data=unmatched_ledger.to_csv(index=False).encode('utf-8'),
        file_name='unmatched_ledger.csv',
        mime='text/csv'
    )
