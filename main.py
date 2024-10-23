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
    def generate_table(self):
        if self.data is None:
            messagebox.showwarning("Error", "Debes cargar un archivo Excel primero")
            return

        # Asume que las columnas son: Equipo_local, Equipo_visitante, Goles_local, Goles_visitante, Goleadores_local, Goleadores_visitante
        table_positions = {}
        table_scorers = {}
        for index, row in self.data.iterrows():
            local_team = row['Equipo_local']
            visit_team = row['Equipo_visitante']
            local_goals = row['Goles_local']
            visit_goals = row['Goles_visitante']
            # Calcular puntos
            if local_goals > visit_goals:
                self.update_table(local_team, 3, local_goals, visit_goals, table_positions)
                self.update_table(visit_team, 0, visit_goals, local_goals, table_positions)
            elif local_goals < visit_goals:
                self.update_table(local_team, 0, local_goals, visit_goals, table_positions)
                self.update_table(visit_team, 3, visit_goals, local_goals, table_positions)
            else:
                self.update_table(local_team, 1, local_goals, visit_goals, table_positions)
                self.update_table(visit_team, 1, visit_goals, local_goals, table_positions)
