import streamlit as st
import pandas as pd

st.set_page_config(page_title="DD Block Directory", page_icon="📍", layout="centered")

st.title("📍 DD Block New Town Directory")
st.write("Kolkata - 700156")

@st.cache_data
def load_data():
    excel_file = "DD_Block_New_Town_Kolkata_Directory.xlsx"
    # Read excel file and find the correct sheet
    xls = pd.ExcelFile(excel_file)
    sheet_to_use = xls.sheet_names[0] # defaults to first sheet
    for sheet in xls.sheet_names:
        if "Directory" in sheet:
            sheet_to_use = sheet
            break
            
    df = pd.read_excel(excel_file, sheet_name=sheet_to_use)
    return df

try:
    raw_df = load_data()
    
    # Locate the header row dynamically (looking for 'Name')
    header_row_idx = 0
    for idx, row in raw_df.iterrows():
        row_str = str(row.values)
        if "Name" in row_str and "Phone" in row_str:
            header_row_idx = idx
            break
            
    # Re-read with correct header row
    excel_file = "DD_Block_New_Town_Kolkata_Directory.xlsx"
    xls = pd.ExcelFile(excel_file)
    sheet_to_use = xls.sheet_names[0]
    for sheet in xls.sheet_names:
        if "Directory" in sheet:
            sheet_to_use = sheet
            break
            
    df = pd.read_excel(excel_file, sheet_name=sheet_to_use, skiprows=header_row_idx)
    df = df.dropna(subset=[df.columns[0]]) # drop empty rows
    
    # Clean column names
    df.columns = [str(c).strip() for c in df.columns]
    
    # Identify key columns
    name_col = next((col for col in df.columns if 'name' in col.lower()), df.columns[0])
    address_col = next((col for col in df.columns if 'address' in col.lower() or 'street' in col.lower()), df.columns[1] if len(df.columns) > 1 else df.columns[0])
    phone_col = next((col for col in df.columns if 'phone' in col.lower() or 'number' in col.lower()), df.columns[-1])

    # Search box
    search_query = st.text_input("🔍 Search by Name, Address, or Phone", "")
    
    if search_query:
        mask = df.astype(str).apply(lambda x: x.str.contains(search_query, case=False, na=False)).any(axis=1)
        filtered_df = df[mask]
    else:
        filtered_df = df

    st.write(f"Showing **{len(filtered_df)}** entries")
    st.divider()

    # Display records
    for index, row in filtered_df.iterrows():
        name = row.get(name_col, "N/A")
        address = row.get(address_col, "N/A")
        phone = row.get(phone_col, "N/A")
        
        if pd.isna(name) or str(name).strip() == "" or str(name).lower() == "nan":
            continue
            
        st.markdown(f"""
        👤 **{name}**  
        📍 {address}  
        📞 `{phone}`
        """)
        st.markdown("---")

except Exception as e:
    st.error(f"An error occurred while loading data: {e}")
