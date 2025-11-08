import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class PCR_Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("PCR Extension Time Calculator")
        
        # Dictionary of enzymes and their rates (bp/sec)
        self.enzyme_rates = {
            "Select enzyme": 0,
            "Manual Entry": "manual",  # Add this line
            "Taq Polymerase": 1000,
            "Pfu Polymerase": 500,
            "Q5 Polymerase": 2000,
            "Phusion Polymerase": 1500
        }
        
        # Create and set up GUI elements
        self.setup_gui()
        
    def setup_gui(self):
        # Create frames for better organization
        input_frame = ttk.Frame(self.root, padding="10")
        input_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Enzyme selection dropdown
        ttk.Label(input_frame, text="Select Enzyme:").grid(row=0, column=0, pady=5)
        self.enzyme_var = tk.StringVar()
        self.enzyme_dropdown = ttk.Combobox(input_frame, 
                                          textvariable=self.enzyme_var,
                                          values=list(self.enzyme_rates.keys()))
        self.enzyme_dropdown.grid(row=0, column=1, pady=5)
        self.enzyme_dropdown.set("Select enzyme")
        self.enzyme_dropdown.bind('<<ComboboxSelected>>', self.on_enzyme_select)
        
        # Manual rate entry (initially hidden)
        ttk.Label(input_frame, text="Manual Rate (bp/sec):").grid(row=1, column=0, pady=5)
        self.rate_entry = ttk.Entry(input_frame)
        self.rate_entry.grid(row=1, column=1, pady=5)
        self.rate_entry.grid_remove()  # Hide initially
        
        # Product length entry
        self.length_label = ttk.Label(input_frame, text="Product Length (bp):")
        self.length_label.grid(row=2, column=0, pady=5)
        self.length_entry = ttk.Entry(input_frame)
        self.length_entry.grid(row=2, column=1, pady=5)
        
        # Calculate button
        ttk.Button(input_frame, 
                  text="Calculate", 
                  command=self.calculate).grid(row=3, column=0, columnspan=2, pady=10)
        
        # Result display
        self.result_var = tk.StringVar()
        ttk.Label(input_frame, textvariable=self.result_var).grid(row=4, column=0, columnspan=2)

    def on_enzyme_select(self, event=None):
        if self.enzyme_var.get() == "Manual Entry":
            self.rate_entry.grid()  # Show rate entry
            self.length_label.grid(row=2, column=0)  # Adjust positions
            self.length_entry.grid(row=2, column=1)
        else:
            self.rate_entry.grid_remove()  # Hide rate entry
            self.length_label.grid(row=1, column=0)  # Restore positions
            self.length_entry.grid(row=1, column=1)

    def calculate(self):
        try:
            # Get selected enzyme rate
            selected_enzyme = self.enzyme_var.get()
            if selected_enzyme == "Select enzyme":
                messagebox.showerror("Error", "Please select an enzyme")
                return
                
            if selected_enzyme == "Manual Entry":
                try:
                    rate = float(self.rate_entry.get())
                    if rate <= 0:
                        messagebox.showerror("Error", "Rate must be greater than 0")
                        return
                except ValueError:
                    messagebox.showerror("Error", "Please enter a valid rate")
                    return
            else:
                rate = self.enzyme_rates[selected_enzyme]
            length = float(self.length_entry.get())
            
            # Calculate extension time
            extension_time = length / rate
            
            # Convert to minutes and seconds
            minutes = int(extension_time // 60)
            seconds = extension_time % 60
            
            # Display result
            if minutes > 0:
                result = f"Extension time: {minutes} min {seconds:.2f} sec"
            else:
                result = f"Extension time: {seconds:.2f} sec"
            
            self.result_var.set(result)
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for product length")
        except ZeroDivisionError:
            messagebox.showerror("Error", "Selected enzyme has no defined rate")

def main():
    root = tk.Tk()
    app = PCR_Calculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()