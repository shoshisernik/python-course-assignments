"""
Tk GUI – asks for:
  • FlyBase gene ID (FBgn…)
  • target organism (drop-down)
  • folder to save the output
Then calls ortholog_fetcher.fetch_and_save().
"""

import tkinter as tk
from tkinter import filedialog, messagebox
from ortholog_fetcher import fetch_and_save

ORGANISMS = [
    "human",          # Homo sapiens
    "mouse",          # Mus musculus
    "rat",            # Rattus norvegicus
    "zebrafish",      # Danio rerio
    "yeast",          # Saccharomyces cerevisiae
    "c. elegans",     # Caenorhabditis elegans
    "arabidopsis",    # Arabidopsis thaliana
]

class OrthologGUI(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        master.title("FlyBase → Ortholog downloader")
        master.geometry("580x340")
        self.pack(fill="both", expand=True)

        self.fbgn_var  = tk.StringVar()
        self.org_var   = tk.StringVar(value=ORGANISMS[0])
        self.path_var  = tk.StringVar()

        self._build_widgets()

    # ---------- UI ----------
    def _build_widgets(self):
        tk.Label(self, text="FlyBase gene ID (e.g. FBgn0000099 – spaces allowed):")\
          .pack(anchor="w", padx=20, pady=(12, 2))
        tk.Entry(self, textvariable=self.fbgn_var, width=46).pack(padx=20)

        tk.Label(self, text="Target organism:").pack(anchor="w", padx=20, pady=(12, 2))
        tk.OptionMenu(self, self.org_var, *ORGANISMS).pack(anchor="w", padx=20)

        tk.Label(self, text="Save folder:").pack(anchor="w", padx=20, pady=(12, 2))
        row = tk.Frame(self); row.pack(fill="x", padx=20)
        self.path_lbl = tk.Label(row, text="No folder selected", fg="gray",
                                 wraplength=380, justify="left")
        self.path_lbl.pack(side="left", fill="x", expand=True)
        tk.Button(row, text="Browse", command=self._browse).pack(side="right")

        tk.Button(self, text="Fetch orthologs", bg="#4CAF50", fg="white",
                  command=self._run).pack(pady=18)

        self.status = tk.Label(self, text="", fg="gray")
        self.status.pack()

    # ---------- callbacks ----------
    def _browse(self):
        folder = filedialog.askdirectory(title="Choose output folder")
        if folder:
            self.path_var.set(folder)
            self.path_lbl.config(text=folder, fg="black")

    def _run(self):
        fbgn      = self.fbgn_var.get()
        organism  = self.org_var.get()
        out_dir   = self.path_var.get()

        if not fbgn.strip():
            messagebox.showerror("Error", "Please enter a FlyBase gene ID.")
            return
        if not out_dir:
            messagebox.showerror("Error", "Please choose an output folder.")
            return

        self.status.config(text="Fetching …")
        self.update_idletasks()

        try:
            out_path = fetch_and_save(fbgn, organism, out_dir)
            self.status.config(text="Done.")
            messagebox.showinfo("Success", f"File created:\n{out_path}")
        except Exception as exc:
            self.status.config(text="Failed.")
            messagebox.showerror("Error", str(exc))

if __name__ == "__main__":
    root = tk.Tk()
    OrthologGUI(root)
    root.mainloop()
