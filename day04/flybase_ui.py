import tkinter as tk
from tkinter import filedialog, messagebox
from flybase_fetcher import fetch_all_and_save


class FlyBaseUI(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master.title("FlyBase Gene Downloader")
        self.master.geometry("560x320")
        self.pack(fill="both", expand=True)

        self.query_var = tk.StringVar()
        self.path_var = tk.StringVar()

        tk.Label(self, text="===== FlyBase Gene Downloader =====",
                 font=("Arial", 14, "bold")).pack(pady=10)

        tk.Label(self, text="Enter gene (symbol or FB ID, e.g., 'wg' or 'FBgn0000099'):") \
            .pack(anchor="w", padx=20)
        tk.Entry(self, textvariable=self.query_var, width=45).pack(padx=20, pady=6)

        tk.Label(self, text="Select folder to save Excel:") \
            .pack(anchor="w", padx=20, pady=(10, 0))

        row = tk.Frame(self)
        row.pack(fill="x", padx=20, pady=6)
        self.path_lbl = tk.Label(row, text="No folder selected", fg="gray", wraplength=380, justify="left")
        self.path_lbl.pack(side="left", fill="x", expand=True)
        tk.Button(row, text="Browse", command=self._browse).pack(side="right")

        tk.Button(self, text="Fetch from FlyBase",
                  bg="#4CAF50", fg="white", width=22,
                  command=self._run).pack(pady=16)

        self.status = tk.Label(self, text="", fg="gray")
        self.status.pack(pady=4)

    def _browse(self):
        folder = filedialog.askdirectory(title="Choose output folder")
        if folder:
            self.path_var.set(folder)
            self.path_lbl.config(text=folder, fg="black")

    def _run(self):
        query = self.query_var.get().strip()
        out_dir = self.path_var.get().strip()
        if not query:
            messagebox.showerror("Error", "Please enter a gene symbol or FlyBase ID.")
            return
        if not out_dir:
            messagebox.showerror("Error", "Please choose an output folder.")
            return

        self.status.config(text="Fetching… please wait.")
        self.master.update_idletasks()

        try:
            out_path, resolved = fetch_all_and_save(query, out_dir)
            msg = f"Saved:\n{out_path}"
            if resolved and resolved != query:
                msg += f"\n\nResolved '{query}' → {resolved}"
            messagebox.showinfo("Success", msg)
            self.status.config(text="Done.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status.config(text="Failed.")


def main():
    root = tk.Tk()
    app = FlyBaseUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
