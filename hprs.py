"""
Patient Record Management System
A simple application to manage patient records using CSV file storage
Developed with Python and CustomTkinter for GUI
"""

# Import required libraries
import customtkinter as ctk  # For modern GUI components
import csv  # For handling CSV file operations
import os  # For file path operations
from datetime import datetime  # For handling dates
from tkinter import messagebox, filedialog  # For dialog boxes
from tkinter import ttk  # For treeview widget

# Configure the appearance of CustomTkinter
ctk.set_appearance_mode("light")  # Can be "light", "dark", or "system"
ctk.set_default_color_theme("green")  # Theme color for the application

class PatientRecordSystem:
    """
    Main class for the Patient Record Management System
    Handles all functionality including GUI, file operations, and data management
    """
    
    def __init__(self):
        """
        Constructor method - initializes the application window and variables
        """
        # Create the main window
        self.window = ctk.CTk()
        self.window.title("Patient Record Management System")
        self.window.geometry("1200x700")
        
        # CSV file name where patient records will be stored
        self.csv_file = "patient_records.csv"
        
        # Define CSV column headers
        self.headers = [
            "Patient ID", 
            "Name", 
            "Age", 
            "Gender", 
            "Contact Number", 
            "Address", 
            "Admission Date", 
            "Disease", 
            "Doctor Assigned", 
            "Room Number"
        ]
        
        # Initialize the CSV file if it doesn't exist
        self.initialize_csv()
        
        # Create the user interface
        self.create_ui()
        
        # Load existing records into the table
        self.load_records()
    
    def initialize_csv(self):
        """
        Creates the CSV file with headers if it doesn't exist
        """
        if not os.path.exists(self.csv_file):
            with open(self.csv_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(self.headers)
    
    def create_ui(self):
        """
        Creates the complete user interface with all components
        """
        # Create main container frame
        main_frame = ctk.CTkFrame(self.window)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create header/title section
        header_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=10, pady=(10, 5))
        
        title_label = ctk.CTkLabel(
            header_frame, 
            text="PATIENT RECORD MANAGEMENT SYSTEM", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(side="left", padx=10)
        
        # Create input section for adding/editing records
        self.create_input_section(main_frame)
        
        # Create button section for various operations
        self.create_button_section(main_frame)
        
        # Create search section
        self.create_search_section(main_frame)
        
        # Create table section to display records
        self.create_table_section(main_frame)
        
        # Create status bar
        self.create_status_bar(main_frame)
    
    def create_input_section(self, parent):
        """
        Creates the input fields for patient information
        """
        input_frame = ctk.CTkFrame(parent)
        input_frame.pack(fill="x", padx=10, pady=5)
        
        # Title for input section
        input_title = ctk.CTkLabel(
            input_frame, 
            text="Patient Information", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        input_title.grid(row=0, column=0, columnspan=5, pady=5, sticky="w")
        
        # Create a dictionary to store input fields
        self.input_fields = {}
        
        # Define field names and their grid positions
        fields = [
            ("Patient ID:", "patient_id", 1, 0),
            ("Name:", "name", 1, 2),
            ("Age:", "age", 1, 4),
            ("Gender:", "gender", 2, 0),
            ("Contact Number:", "contact", 2, 2),
            ("Address:", "address", 3, 0),
            ("Admission Date:", "admission_date", 3, 2),
            ("Disease:", "disease", 4, 0),
            ("Doctor Assigned:", "doctor", 4, 2),
            ("Room Number:", "room", 5, 0)
        ]
        
        # Create labels and entry fields
        for label_text, field_name, row, col in fields:
            # Label
            label = ctk.CTkLabel(input_frame, text=label_text)
            label.grid(row=row, column=col, padx=5, pady=5, sticky="e")
            
            # Entry field
            entry = ctk.CTkEntry(input_frame, width=200)
            entry.grid(row=row, column=col+1, padx=5, pady=5, sticky="w")
            
            # Store entry in dictionary for easy access
            self.input_fields[field_name] = entry
        
        # Set default admission date to today
        self.input_fields["admission_date"].insert(0, datetime.now().strftime("%Y-%m-%d"))
    
    def create_button_section(self, parent):
        """
        Creates buttons for various operations
        """
        button_frame = ctk.CTkFrame(parent)
        button_frame.pack(fill="x", padx=10, pady=5)
        
        # Create buttons with their commands
        buttons = [
            ("Add Record", self.add_record, "green"),
            ("Update Record", self.update_record, "blue"),
            ("Delete Record", self.delete_record, "red"),
            ("Clear Fields", self.clear_fields, "gray"),
            ("Export to CSV", self.export_records, "purple"),
            ("Refresh", self.load_records, "orange")
        ]
        
        for i, (text, command, color) in enumerate(buttons):
            btn = ctk.CTkButton(
                button_frame,
                text=text,
                command=command,
                fg_color=color,
                hover_color=self.get_hover_color(color),
                width=120
            )
            btn.grid(row=0, column=i, padx=5, pady=5)
    
    def get_hover_color(self, color):
        """
        Returns hover color based on button color
        """
        hover_colors = {
            "green": "#2e7d32",
            "blue": "#1565c0",
            "red": "#b71c1c",
            "gray": "#424242",
            "purple": "#4a1b6d",
            "orange": "#bf360c"
        }
        return hover_colors.get(color, color)
    
    def create_search_section(self, parent):
        """
        Creates search functionality section
        """
        search_frame = ctk.CTkFrame(parent)
        search_frame.pack(fill="x", padx=10, pady=5)
        
        # Search label
        search_label = ctk.CTkLabel(search_frame, text="Search:", font=ctk.CTkFont(weight="bold"))
        search_label.grid(row=0, column=0, padx=5, pady=5)
        
        # Search by dropdown
        self.search_by = ctk.CTkComboBox(
            search_frame,
            values=["Patient ID", "Name", "Disease", "Doctor Assigned"],
            width=150
        )
        self.search_by.grid(row=0, column=1, padx=5, pady=5)
        self.search_by.set("Name")
        
        # Search entry
        self.search_entry = ctk.CTkEntry(search_frame, width=300, placeholder_text="Enter search term...")
        self.search_entry.grid(row=0, column=2, padx=5, pady=5)
        
        # Search button
        search_btn = ctk.CTkButton(
            search_frame,
            text="Search",
            command=self.search_records,
            width=100
        )
        search_btn.grid(row=0, column=3, padx=5, pady=5)
        
        # Show all button
        show_all_btn = ctk.CTkButton(
            search_frame,
            text="Show All",
            command=self.load_records,
            width=100,
            fg_color="gray"
        )
        show_all_btn.grid(row=0, column=4, padx=5, pady=5)
    
    def create_table_section(self, parent):
        """
        Creates table to display patient records
        """
        table_frame = ctk.CTkFrame(parent)
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Create Treeview widget for displaying records
        self.tree = ttk.Treeview(table_frame, columns=self.headers, show="headings", height=15)
        
        # Create scrollbars
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        # Configure columns
        for col in self.headers:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, minwidth=80)
        
        # Grid layout for tree and scrollbars
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        
        # Configure grid weights
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        # Bind select event to populate fields
        self.tree.bind('<<TreeviewSelect>>', self.on_record_select)
    
    def create_status_bar(self, parent):
        """
        Creates status bar at the bottom
        """
        status_frame = ctk.CTkFrame(parent, height=30)
        status_frame.pack(fill="x", padx=10, pady=5)
        status_frame.pack_propagate(False)
        
        self.status_label = ctk.CTkLabel(
            status_frame,
            text="Ready",
            font=ctk.CTkFont(size=12)
        )
        self.status_label.pack(side="left", padx=10)
        
        self.record_count_label = ctk.CTkLabel(
            status_frame,
            text="Total Records: 0",
            font=ctk.CTkFont(size=12)
        )
        self.record_count_label.pack(side="right", padx=10)
    
    def validate_input(self):
        """
        Validates the input fields
        Returns: (is_valid, error_message)
        """
        # Check required fields
        required_fields = ["patient_id", "name", "age"]
        for field in required_fields:
            if not self.input_fields[field].get().strip():
                return False, f"{field.replace('_', ' ').title()} is required"
        
        # Validate age (should be a number)
        age = self.input_fields["age"].get().strip()
        try:
            age_int = int(age)
            if age_int < 0 or age_int > 150:
                return False, "Age must be between 0 and 150"
        except ValueError:
            return False, "Age must be a valid number"
        
        return True, "Valid"
    
    def add_record(self):
        """
        Adds a new patient record to the CSV file
        """
        # Validate input
        is_valid, message = self.validate_input()
        if not is_valid:
            messagebox.showerror("Validation Error", message)
            return
        
        # Get all field values
        new_record = []
        for header in self.headers:
            field_name = header.lower().replace(" ", "_")
            if field_name in self.input_fields:
                value = self.input_fields[field_name].get().strip()
            else:
                value = ""
            new_record.append(value)
        
        # Check if Patient ID already exists
        if self.check_duplicate_id(new_record[0]):
            messagebox.showerror("Error", f"Patient ID {new_record[0]} already exists!")
            return
        
        try:
            # Append to CSV file
            with open(self.csv_file, 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(new_record)
            
            # Clear input fields
            self.clear_fields()
            
            # Reload records
            self.load_records()
            
            # Show success message
            messagebox.showinfo("Success", "Patient record added successfully!")
            self.status_label.configure(text=f"Record added: {new_record[1]}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add record: {str(e)}")
    
    def update_record(self):
        """
        Updates an existing patient record
        """
        # Check if a record is selected
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a record to update")
            return
        
        # Validate input
        is_valid, message = self.validate_input()
        if not is_valid:
            messagebox.showerror("Validation Error", message)
            return
        
        # Get selected item values
        selected_item = self.tree.item(selected[0])
        old_values = selected_item['values']
        
        # Get updated values
        updated_record = []
        for header in self.headers:
            field_name = header.lower().replace(" ", "_")
            if field_name in self.input_fields:
                value = self.input_fields[field_name].get().strip()
            else:
                value = ""
            updated_record.append(value)
        
        # Read all records
        records = []
        with open(self.csv_file, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            records = list(reader)
        
        # Update the matching record
        updated = False
        for i, record in enumerate(records[1:], 1):  # Skip header
            if record[0] == old_values[0]:  # Match by Patient ID
                records[i] = updated_record
                updated = True
                break
        
        if updated:
            # Write back to file
            with open(self.csv_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerows(records)
            
            # Reload and show success
            self.load_records()
            messagebox.showinfo("Success", "Record updated successfully!")
            self.status_label.configure(text=f"Record updated: {updated_record[1]}")
        else:
            messagebox.showerror("Error", "Record not found in database")
    
    def delete_record(self):
        """
        Deletes a selected patient record
        """
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a record to delete")
            return
        
        # Confirm deletion
        if not messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this record?"):
            return
        
        # Get selected patient ID
        selected_item = self.tree.item(selected[0])
        patient_id = selected_item['values'][0]
        patient_name = selected_item['values'][1]
        
        # Read all records
        records = []
        with open(self.csv_file, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            records = list(reader)
        
        # Filter out the record to delete
        header = records[0]
        data_records = records[1:]
        new_records = [record for record in data_records if record[0] != patient_id]
        
        # Write back to file
        with open(self.csv_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(new_records)
        
        # Reload and show success
        self.load_records()
        messagebox.showinfo("Success", "Record deleted successfully!")
        self.status_label.configure(text=f"Record deleted: {patient_name}")
    
    def clear_fields(self):
        """
        Clears all input fields
        """
        for field in self.input_fields.values():
            field.delete(0, 'end')
        
        # Set default admission date
        self.input_fields["admission_date"].insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.status_label.configure(text="Fields cleared")
    
    def load_records(self):
        """
        Loads and displays all records from CSV file
        """
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            # Read records from CSV
            records = []
            with open(self.csv_file, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                records = list(reader)
            
            # Insert records into treeview
            for record in records:
                if any(record):  # Check if record is not empty
                    self.tree.insert('', 'end', values=record)
            
            # Update record count
            count = len(records)
            self.record_count_label.configure(text=f"Total Records: {count}")
            self.status_label.configure(text=f"Loaded {count} records")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load records: {str(e)}")
    
    def search_records(self):
        """
        Searches records based on selected criteria
        """
        search_term = self.search_entry.get().strip().lower()
        if not search_term:
            self.load_records()
            return
        
        search_field = self.search_by.get()
        
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            # Read records
            with open(self.csv_file, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                headers = next(reader)  # Skip header
                
                # Find column index for search field
                col_index = headers.index(search_field)
                
                # Search and display matching records
                found_count = 0
                for record in reader:
                    if col_index < len(record) and search_term in record[col_index].lower():
                        self.tree.insert('', 'end', values=record)
                        found_count += 1
            
            # Update status
            self.record_count_label.configure(text=f"Found: {found_count} records")
            self.status_label.configure(text=f"Searched for '{search_term}' in {search_field}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Search failed: {str(e)}")
    
    def on_record_select(self, event):
        """
        Handles record selection from table
        Populates input fields with selected record data
        """
        selected = self.tree.selection()
        if not selected:
            return
        
        # Get selected record values
        selected_item = self.tree.item(selected[0])
        values = selected_item['values']
        
        # Populate input fields
        for i, header in enumerate(self.headers):
            field_name = header.lower().replace(" ", "_")
            if field_name in self.input_fields and i < len(values):
                self.input_fields[field_name].delete(0, 'end')
                self.input_fields[field_name].insert(0, values[i])
    
    def check_duplicate_id(self, patient_id):
        """
        Checks if a patient ID already exists in the database
        """
        try:
            with open(self.csv_file, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                for record in reader:
                    if record and record[0] == patient_id:
                        return True
        except:
            pass
        return False
    
    def export_records(self):
        """
        Exports records to a new CSV file
        """
        # Ask for file location
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Export Records As"
        )
        
        if filename:
            try:
                # Copy current file to new location
                import shutil
                shutil.copy2(self.csv_file, filename)
                messagebox.showinfo("Success", f"Records exported to {filename}")
                self.status_label.configure(text=f"Exported to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Export failed: {str(e)}")
    
    def run(self):
        """
        Starts the application
        """
        self.window.mainloop()

# Main entry point
if __name__ == "__main__":
    # Create and run the application
    app = PatientRecordSystem()
    app.run()