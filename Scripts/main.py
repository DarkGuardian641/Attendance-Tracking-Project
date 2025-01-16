import tkinter as tk
from tkinter import ttk
import mysql.connector
from datetime import datetime
import serial
import threading
import time

class AttendanceUI:
    def __init__(self):
        self.app = tk.Tk()
        self.app.title("RFID Attendance System")
        self.app.geometry("800x600")
        
        # Create main frame
        self.main_frame = ttk.Frame(self.app, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Status label
        self.status_label = ttk.Label(self.main_frame, text="Waiting for RFID scan...", font=('Arial', 12))
        self.status_label.pack(pady=10)
        
        # Create Treeview
        self.tree_frame = ttk.Frame(self.main_frame)
        self.tree_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create Treeview with scrollbar
        self.tree = ttk.Treeview(self.tree_frame, columns=("ID", "Student Name", "Timestamp"), show="headings", height=0)  # height=0 means show all items
        self.tree.heading("ID", text="ID")
        self.tree.heading("Student Name", text="Student Name")
        self.tree.heading("Timestamp", text="Timestamp")
        
        # Configure column widths as proportions of total width
        self.tree.column("ID", width=100, minwidth=50)
        self.tree.column("Student Name", width=300, minwidth=200)
        self.tree.column("Timestamp", width=200, minwidth=150)
        
        # Add vertical scrollbar
        self.v_scrollbar = ttk.Scrollbar(self.tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.v_scrollbar.set)
        
        # Add horizontal scrollbar
        self.h_scrollbar = ttk.Scrollbar(self.tree_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(xscrollcommand=self.h_scrollbar.set)
        
        # Pack scrollbars and treeview
        self.v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Database connection
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="root",
            database="attendance"
        )
        self.cursor = self.db.cursor(buffered=True)
        
        # Serial connection
        try:
            self.ser = serial.Serial('COM9', 9600)
            self.status_label.config(text="RFID Reader Connected")
        except:
            self.status_label.config(text="Failed to connect to RFID Reader")
        
        # Add pagination controls
        self.page_frame = ttk.Frame(self.main_frame)
        self.page_frame.pack(pady=5)
        
        self.records_per_page = 100  # Number of records to load at once
        self.current_page = 1
        
        ttk.Button(self.page_frame, text="Previous", command=self.prev_page).pack(side=tk.LEFT, padx=5)
        self.page_label = ttk.Label(self.page_frame, text="Page 1")
        self.page_label.pack(side=tk.LEFT, padx=5)
        ttk.Button(self.page_frame, text="Next", command=self.next_page).pack(side=tk.LEFT, padx=5)
        
        # Start threads
        self.running = True
        self.rfid_thread = threading.Thread(target=self.rfid_loop, daemon=True)
        self.refresh_thread = threading.Thread(target=self.refresh_loop, daemon=True)
        self.rfid_thread.start()
        self.refresh_thread.start()
        
        # Bind close event
        self.app.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Initial data load
        self.refresh_data()
    
    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.refresh_data()
    
    def next_page(self):
        self.current_page += 1
        self.refresh_data()
    
    def refresh_data(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Calculate offset
        offset = (self.current_page - 1) * self.records_per_page
            
        # Fetch and insert new data
        try:
            # Get total count
            self.cursor.execute("SELECT COUNT(*) FROM records")
            total_records = self.cursor.fetchone()[0]
            
            # Fetch page data
            self.cursor.execute("""
                SELECT id, student_name, timestamp 
                FROM records 
                ORDER BY timestamp DESC 
                LIMIT %s OFFSET %s
            """, (self.records_per_page, offset))
            
            records = self.cursor.fetchall()
            
            if not records and self.current_page > 1:
                self.current_page -= 1
                self.refresh_data()
                return
            
            for record in records:
                self.tree.insert('', 'end', values=record)
            
            total_pages = (total_records + self.records_per_page - 1) // self.records_per_page
            self.page_label.config(text=f"Page {self.current_page} of {total_pages}")
            
        except mysql.connector.Error as err:
            self.status_label.config(text=f"Database Error: {err}")
    
    def read_rfid(self):
        if self.ser.in_waiting > 0:
            rfid_data = self.ser.readline().decode('utf-8').strip()
            return rfid_data
        return None
    
    def rfid_loop(self):
        while self.running:
            rfid_data = self.read_rfid()
            if rfid_data and rfid_data != "Place your RFID card/tag near the reader...":
                try:
                    self.cursor.execute("SELECT student_name FROM students WHERE rfid_uid = %s", (rfid_data,))
                    result = self.cursor.fetchone()
                    
                    if result:
                        student_name = result[0]
                        self.cursor.execute("INSERT INTO records (student_name, timestamp) VALUES (%s, NOW())", (student_name,))
                        self.db.commit()
                        self.status_label.config(text=f"Recorded: {student_name}")
                        # Refresh to show new entry
                        self.current_page = 1  # Reset to first page to show newest entry
                        self.app.after(0, self.refresh_data)
                    else:
                        self.status_label.config(text="Unknown RFID Tag")
                        
                except mysql.connector.Error as err:
                    self.status_label.config(text=f"Error: {err}")
    
    def refresh_loop(self):
        while self.running:
            time.sleep(5)  # Refresh every 5 seconds instead of 1 for better performance
            self.app.after(0, self.refresh_data)
    
    def on_closing(self):
        self.running = False
        if hasattr(self, 'ser'):
            self.ser.close()
        self.db.close()
        self.app.destroy()
    
    def run(self):
        self.app.mainloop()

if __name__ == "__main__":
    app = AttendanceUI()
    app.run()