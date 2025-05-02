import streamlit as st
import pandas as pd

# Load cost centre reference
vehicle_map = pd.read_csv("vehicle_cost_centres.csv")
vehicle_map['registration'] = vehicle_map['registration'].str.upper().str.strip()
vehicle_map['cost_centre'] = vehicle_map['cost_centre'].replace({'Shep': 'Shepp'})

# Upload section
st.title("Shell Fuel Cost Centre Bot")
uploaded_file = st.file_uploader("Upload the Shell Excel file (.xlsx)", type="xlsx")

if uploaded_file:
    df = pd.read_excel(uploaded_file, sheet_name="Export")
    df.columns = [col.lower() for col in df.columns]
    df['registration'] = df['registration'].str.upper().str.strip()
    df['registration'] = df['registration'].replace({
        'EAS90L': 'ESA90L',
        '1QQ4UK': '2BK7CA',
        '1UG4PJ': 'EOS53F'
    })

    merged = df.merge(vehicle_map, on='registration', how='left')
    merged['cost_centre'] = merged['cost_centre'].replace({'Shep': 'Shepp'})

    summary = (
        merged.groupby('cost_centre')['totalshellcardamount(incl)']
        .sum()
        .round(2)
        .reset_index()
        .sort_values(by='totalshellcardamount(incl)', ascending=False)
    )

    total = pd.DataFrame([{
        'cost_centre': 'Total',
        'totalshellcardamount(incl)': merged['totalshellcardamount(incl)'].sum().round(2)
    }])
    final = pd.concat([summary, total], ignore_index=True)

    st.success("✅ Processed Successfully")
    st.dataframe(final)

    csv = final.to_csv(index=False).encode('utf-8')
    st.download_button("Download Summary CSV", data=csv, file_name="fuel_cost_summary.csv")
