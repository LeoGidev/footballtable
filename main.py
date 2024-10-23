import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
from openpyxl import load_workbook

class FootballApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tabla de posiciones y goleadores")
        self.root.geometry("400x200")
        self.upload_button = tk.Button(self.root, text="Cargar archivo Excel", command=self.upload_file)
        self.upload_button.pack(pady=20)
        self.generate_button = tk.Button(self.root, text="Generar tabla de posiciones", command=self.generate_table)
        self.generate_button.pack(pady=20)
        self.file_path = None
        self.data = None
    def upload_file(self):
        self.file_path = filedialog.askopenfilename(title="Selecciona el archivo Excel", filetypes=[("Excel files", "*.xlsx")])
        if self.file_path:
            self.data = pd.read_excel(self.file_path)
            messagebox.showinfo("Cargado", "Archivo cargado correctamente")