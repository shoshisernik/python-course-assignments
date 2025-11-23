import tkinter as tk
from tkinter import filedialog, messagebox
from code_geneloc_flybase import fetch_gene_info_and_save

#Instructions for use:
#This code provides a simple user interface that the other code in this 
#directory can use to get input from the user.
#Provide the FlyBase ID of the gene of interest and the path of the folder in which you would like the data downloaded.
#Example FlyBase IDs: FBgn0000099 (ap), FBgn0003848 (wg), FBgn0005561 (so)

class GeneLocApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FlyBase Gene Fetcher")
        self.root.geometry("500x300")
        self.selected_path = tk.StringVar()

        # Title
        title_label = tk.Label(root, text="===== FlyBase Gene Fetcher =====", font=("Arial", 14, "bold"))
        title_label.pack(pady=10)

        # FlyBase ID input
        fbgn_label = tk.Label(root, text="Enter FlyBase ID (e.g., 'FBgn0000099', 'FBgn0003848'):")
        fbgn_label.pack(anchor="w", padx=20, pady=5)
        self.fbgn_entry = tk.Entry(root, width=40)
        self.fbgn_entry.pack(padx=20, pady=5)

        # Output path section
        path_label = tk.Label(root, text="Select folder to save Excel file:")
        path_label.pack(anchor="w", padx=20, pady=(15, 5))
        
        path_frame = tk.Frame(root)
        path_frame.pack(padx=20, pady=5, fill="x")
        
        self.path_display = tk.Label(path_frame, text="No folder selected", fg="gray", wraplength=350, justify="left")
        self.path_display.pack(side="left", fill="x", expand=True)
        
        browse_button = tk.Button(path_frame, text="Browse", command=self.browse_folder)
        browse_button.pack(side="right", padx=5)

        # Submit button
        submit_button = tk.Button(root, text="Fetch Gene Info", command=self.submit, bg="#4CAF50", fg="white", width=20)
        submit_button.pack(pady=20)

    def browse_folder(self):
        folder = filedialog.askdirectory(title="Select folder to save Excel file")
        if folder:
            self.selected_path.set(folder)
            self.path_display.config(text=folder, fg="black")

    def submit(self):
        fbgn_id = self.fbgn_entry.get().strip()
        output_path = self.selected_path.get()

        if not fbgn_id:
            messagebox.showerror("Error", "Please enter a FlyBase ID.")
            return
        
        if not output_path:
            messagebox.showerror("Error", "Please select a folder path.")
            return

        try:
            excel_file = fetch_gene_info_and_save(fbgn_id, output_path)
            messagebox.showinfo("Success", f"File saved at:\n{excel_file}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{e}")

def main():
    root = tk.Tk()
    app = GeneLocApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
