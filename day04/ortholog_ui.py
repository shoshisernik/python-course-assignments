"""
Tk GUI for Drosophila-gene ortholog lookup
------------------------------------------

• enter a FlyBase *gene* ID (FBgn…)
• choose an organism (human, mouse, yeast, C. elegans, …)
• browse for a folder
• click “Fetch” → calls ortholog_fetcher.fetch_and_save()
"""

import tkinter as tk
from tkinter import filedialog, messagebox
from ortholog_fetcher import fetch_and_save


ORGANISMS = [
    "human",          # Homo sapiens (9606)
    "mouse",          # Mus musculus (10090)
    "rat",            # Rattus norvegicus (10116)
    "zebrafish",      # Danio rerio (7955)
    "yeast",          # Saccharomyces cerevisiae (559292)
    "c. elegans",     # Caenorhabditis elegans (6239)
    "arabidopsis"     # Arabidopsis thaliana (3702)
]


class OrthologGUI(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        master.title("FlyBase → Ortholog downloader (DIOPT)")
        master.geometry("560x320")
        self.pack(fill="both", expand=True)

        self.fbgn_var  = tk.StringVar()
        self.org_var   = tk.StringVar(value=ORGANISMS[0])
        self.path_var  = tk.StringVar()

        self._build_widgets()

    # -------------  UI helpers  -------------
    def _build_widgets(self):
        tk.Label(self, text="Drosophila gene (FBgn…):").pack(anchor="w", padx=20, pady=(12, 2))
        tk.Entry(self, textvariable=self.fbgn_var, width=46).pack(padx=20)

        tk.Label(self, text="Target organism:").pack(anchor="w", padx=20, pady=(12, 2))
        tk.OptionMenu(self, self.org_var, *ORGANISMS).pack(padx=20, anchor="w")

        tk.Label(self, text="Save folder:").pack(anchor="w", padx=20, pady=(12, 2))
        path_row = tk.Frame(self); path_row.pack(fill="x", padx=20)
        self.path_lbl = tk.Label(path_row, text="No folder selected", fg="gray", wraplength=360, justify="left")
        self.path_lbl.pack(side="left", fill="x", expand=True)
        tk.Button(path_row, text="Browse", command=self._browse).pack(side="right")

        tk.Button(self, text="Fetch orthologs", bg="#4CAF50", fg="white",
                  command=self._run).pack(pady=18)

        self.status = tk.Label(self, text="", fg="gray")
        self.status.pack()

    def _browse(self):
        folder = filedialog.askdirectory(title="Choose output folder")
        if folder:
            self.path_var.set(folder)
            self.path_lbl.config(text=folder, fg="black")

    def _run(self):
        fbgn = self.fbgn_var.get().strip()
        organism = self.org_var.get()
        out_dir = self.path_var.get().strip()

        if not fbgn:
            messagebox.showerror("Error", "Please enter a FlyBase gene ID (FBgn…).")
            return
        if not out_dir:
            messagebox.showerror("Error", "Please choose an output folder.")
            return

        self.status.config(text="Fetching…")
        self.update_idletasks()

        try:
            out_path = fetch_and_save(fbgn, organism, out_dir)
            messagebox.showinfo("Success", f"File created:\n{out_path}")
            self.status.config(text="Done.")
        except Exception as exc:
            messagebox.showerror("Error", str(exc))
            self.status.config(text="Failed.")


if __name__ == "__main__":
    tk.Tk().withdraw()          # prevents a ghost-window flash on Windows
    root = tk.Tk()
    OrthologGUI(root)
    root.mainloop()
