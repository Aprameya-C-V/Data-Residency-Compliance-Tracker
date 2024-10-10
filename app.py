import streamlit as st
import pandas as pd

# Constants for compliance rules
COMPLIANCE_RULES = {
    "GDPR": ["EU", "EEA"],  # Example regions for GDPR compliance
    "CCPA": ["California"]  # Example regions for CCPA compliance
}


def check_compliance(data):
    """Check compliance based on predefined rules."""
    non_compliant_entries = []

    for index, row in data.iterrows():
        region = row['Region']
        if region not in COMPLIANCE_RULES.get(row['Regulation'], []):
            non_compliant_entries.append(row)

    return non_compliant_entries

# Streamlit app layout
st.title("Data Residency Compliance Tracker")

# Upload data inventory CSV
st.subheader("Upload Data Inventory")
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file:
    # Read the CSV file
    data = pd.read_csv(uploaded_file)

    # Display the uploaded data
    st.write("### Uploaded Data", data)

    # Ensure required columns are present
    if 'Region' in data.columns and 'Regulation' in data.columns:
        # Check compliance
        st.subheader("Compliance Check")
        non_compliant_entries = check_compliance(data)

        # Display compliance results
        if non_compliant_entries:
            st.write("### Non-Compliant Entries")
            st.write(pd.DataFrame(non_compliant_entries))
            st.warning("There are non-compliant entries! Please review.")
        else:
            st.success("All entries are compliant.")

        # Generate Report
        st.subheader("Generate Compliance Report")
        if st.button("Generate Report"):
            report = data.copy()
            report['Compliance Status'] = [
                "Compliant" if row['Region'] in COMPLIANCE_RULES.get(row['Regulation'], []) else "Non-Compliant" for
                index, row in data.iterrows()]
            report.to_csv("compliance_report.csv", index=False)
            st.success("Report generated! You can download it below:")
            st.download_button("Download Report", data=report.to_csv(), file_name='compliance_report.csv',
                               mime='text/csv')
    else:
        st.error("Uploaded CSV must contain 'Region' and 'Regulation' columns.")
