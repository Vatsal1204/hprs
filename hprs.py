"""
Patient Record Management System - Web Version
For Streamlit Cloud deployment
"""

import streamlit as st
import pandas as pd
import csv
import os
from datetime import datetime
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Patient Record Management System",
    page_icon="🏥",
    layout="wide"
)

class PatientRecordSystem:
    def __init__(self):
        self.csv_file = "patient_records.csv"
        self.headers = [
            "Patient ID", "Name", "Age", "Gender", "Contact Number",
            "Address", "Admission Date", "Disease", "Doctor Assigned", "Room Number"
        ]
        self.initialize_csv()
    
    def initialize_csv(self):
        """Create CSV file with headers if it doesn't exist"""
        if not os.path.exists(self.csv_file):
            df = pd.DataFrame(columns=self.headers)
            df.to_csv(self.csv_file, index=False)
    
    def load_data(self):
        """Load data from CSV"""
        try:
            df = pd.read_csv(self.csv_file)
            return df
        except:
            return pd.DataFrame(columns=self.headers)
    
    def save_data(self, df):
        """Save data to CSV"""
        df.to_csv(self.csv_file, index=False)
    
    def check_duplicate_id(self, patient_id):
        """Check if Patient ID exists"""
        df = self.load_data()
        return patient_id in df['Patient ID'].values if not df.empty else False

# Initialize the system
system = PatientRecordSystem()

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        background-color: #2E86AB;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        color: white;
        margin-bottom: 20px;
    }
    .stat-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="main-header">
        <h1>🏥 Patient Record Management System</h1>
        <p>Efficiently manage patient records with ease</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar for navigation
st.sidebar.title("📋 Navigation")
page = st.sidebar.radio(
    "Go to",
    ["Dashboard", "Add Patient", "View Records", "Search", "Statistics", "Export Data"]
)

# Dashboard
if page == "Dashboard":
    st.header("📊 Dashboard")
    
    df = system.load_data()
    
    # Statistics cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
            <div class="stat-card">
                <h3>Total Patients</h3>
                <h2>{}</h2>
            </div>
        """.format(len(df)), unsafe_allow_html=True)
    
    with col2:
        male_count = len(df[df['Gender'].str.lower().isin(['male', 'm'])]) if not df.empty else 0
        st.markdown("""
            <div class="stat-card">
                <h3>Male Patients</h3>
                <h2>{}</h2>
            </div>
        """.format(male_count), unsafe_allow_html=True)
    
    with col3:
        female_count = len(df[df['Gender'].str.lower().isin(['female', 'f'])]) if not df.empty else 0
        st.markdown("""
            <div class="stat-card">
                <h3>Female Patients</h3>
                <h2>{}</h2>
            </div>
        """.format(female_count), unsafe_allow_html=True)
    
    with col4:
        avg_age = round(df['Age'].mean(), 1) if not df.empty and 'Age' in df.columns else 0
        st.markdown("""
            <div class="stat-card">
                <h3>Average Age</h3>
                <h2>{}</h2>
            </div>
        """.format(avg_age), unsafe_allow_html=True)
    
    # Recent records
    st.subheader("📋 Recent Records")
    if not df.empty:
        st.dataframe(df.tail(5), use_container_width=True)
    else:
        st.info("No records found. Add your first patient record!")

# Add Patient
elif page == "Add Patient":
    st.header("➕ Add New Patient Record")
    
    with st.form("patient_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            patient_id = st.text_input("Patient ID *")
            name = st.text_input("Full Name *")
            age = st.number_input("Age *", min_value=0, max_value=150, value=25)
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            contact = st.text_input("Contact Number")
        
        with col2:
            address = st.text_area("Address")
            admission_date = st.date_input("Admission Date", datetime.now())
            disease = st.text_input("Disease")
            doctor = st.text_input("Doctor Assigned")
            room = st.text_input("Room Number")
        
        submitted = st.form_submit_button("Add Patient Record")
        
        if submitted:
            if not patient_id or not name:
                st.error("Patient ID and Name are required fields!")
            elif system.check_duplicate_id(patient_id):
                st.error(f"Patient ID {patient_id} already exists!")
            else:
                new_record = pd.DataFrame([[
                    patient_id, name, age, gender, contact, address,
                    admission_date.strftime("%Y-%m-%d"), disease, doctor, room
                ]], columns=system.headers)
                
                df = system.load_data()
                df = pd.concat([df, new_record], ignore_index=True)
                system.save_data(df)
                
                st.success(f"✅ Patient {name} added successfully!")
                st.balloons()

# View Records
elif page == "View Records":
    st.header("📋 All Patient Records")
    
    df = system.load_data()
    
    if df.empty:
        st.warning("No records found in the database.")
    else:
        # Filters
        with st.expander("🔍 Filter Records"):
            col1, col2, col3 = st.columns(3)
            with col1:
                if 'Gender' in df.columns:
                    gender_filter = st.multiselect("Filter by Gender", df['Gender'].unique())
            with col2:
                if 'Disease' in df.columns:
                    disease_filter = st.multiselect("Filter by Disease", df['Disease'].unique())
            with col3:
                if 'Doctor Assigned' in df.columns:
                    doctor_filter = st.multiselect("Filter by Doctor", df['Doctor Assigned'].unique())
        
        # Apply filters
        filtered_df = df.copy()
        if gender_filter:
            filtered_df = filtered_df[filtered_df['Gender'].isin(gender_filter)]
        if disease_filter:
            filtered_df = filtered_df[filtered_df['Disease'].isin(disease_filter)]
        if doctor_filter:
            filtered_df = filtered_df[filtered_df['Doctor Assigned'].isin(doctor_filter)]
        
        # Display records
        st.dataframe(filtered_df, use_container_width=True)
        st.info(f"Showing {len(filtered_df)} of {len(df)} records")

# Search
elif page == "Search":
    st.header("🔍 Search Records")
    
    search_by = st.selectbox("Search by", ["Patient ID", "Name", "Disease", "Doctor Assigned"])
    search_term = st.text_input(f"Enter {search_by} to search")
    
    if search_term:
        df = system.load_data()
        if not df.empty:
            # Perform search
            mask = df[search_by].astype(str).str.contains(search_term, case=False, na=False)
            results = df[mask]
            
            if not results.empty:
                st.success(f"Found {len(results)} matching record(s)")
                st.dataframe(results, use_container_width=True)
            else:
                st.warning(f"No records found matching '{search_term}'")

# Statistics
elif page == "Statistics":
    st.header("📊 Statistical Analysis")
    
    df = system.load_data()
    
    if df.empty:
        st.warning("No data available for statistics.")
    else:
        col1, col2 = st.columns(2)
        
        with col1:
            # Gender distribution
            st.subheader("Gender Distribution")
            gender_counts = df['Gender'].value_counts()
            fig_gender = px.pie(values=gender_counts.values, names=gender_counts.index, 
                               title="Patients by Gender")
            st.plotly_chart(fig_gender, use_container_width=True)
        
        with col2:
            # Age distribution
            st.subheader("Age Distribution")
            fig_age = px.histogram(df, x='Age', nbins=20, 
                                  title="Age Distribution of Patients")
            st.plotly_chart(fig_age, use_container_width=True)
        
        # Disease statistics
        st.subheader("Disease Statistics")
        disease_counts = df['Disease'].value_counts().head(10)
        fig_disease = px.bar(x=disease_counts.values, y=disease_counts.index,
                            orientation='h', title="Top 10 Diseases")
        st.plotly_chart(fig_disease, use_container_width=True)

# Export Data
elif page == "Export Data":
    st.header("📥 Export Data")
    
    df = system.load_data()
    
    if df.empty:
        st.warning("No data to export.")
    else:
        st.write("Preview of data to be exported:")
        st.dataframe(df.head(), use_container_width=True)
        
        # Export options
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📄 Export as CSV", use_container_width=True):
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"patient_records_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
        
        with col2:
            if st.button("📊 Export as Excel", use_container_width=True):
                output = pd.ExcelWriter('temp.xlsx', engine='openpyxl')
                df.to_excel(output, index=False, sheet_name='Patients')
                output.close()
                
                with open('temp.xlsx', 'rb') as f:
                    st.download_button(
                        label="Download Excel",
                        data=f,
                        file_name=f"patient_records_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("### 📌 Quick Actions")
if st.sidebar.button("🔄 Refresh Data"):
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("### ℹ️ About")
st.sidebar.info(
    "This Patient Record Management System helps healthcare "
    "facilities efficiently manage patient records. All data "
    "is stored locally in CSV format."
)
