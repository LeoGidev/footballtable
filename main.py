import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from openpyxl import load_workbook
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
import os

class FootballApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tabla de posiciones y goleadores")
        self.root.geometry("500x300")
        self.root.configure(bg="#2E4053")

        # Estilos personalizados
        style = ttk.Style()
        style.configure('TButton', font=('Helvetica', 12), padding=10)
        style.configure('TLabel', font=('Helvetica', 12), foreground="#ECF0F1", background="#2E4053")

        self.upload_button = ttk.Button(self.root, text="Cargar archivo Excel", command=self.upload_file)
        self.upload_button.pack(pady=10)
        
        self.generate_button = ttk.Button(self.root, text="Generar tablas e imágenes", command=self.generate_table)
        self.generate_button.pack(pady=10)

        self.status_label = ttk.Label(self.root, text="")
        self.status_label.pack(pady=20)
        
        self.file_path = None
        self.data = None

    def upload_file(self):
        self.file_path = filedialog.askopenfilename(title="Selecciona el archivo Excel", filetypes=[("Excel files", "*.xlsx")])
        if self.file_path:
            self.data = pd.read_excel(self.file_path)
            messagebox.showinfo("Cargado", "Archivo cargado correctamente")
            self.status_label.config(text="Archivo cargado: " + os.path.basename(self.file_path))

     def select_background_image(self):

    def generate_table(self):
        if self.data is None:
            messagebox.showwarning("Error", "Debes cargar un archivo Excel primero")
            return

        table_positions = {}
        table_scorers = {}

        for index, row in self.data.iterrows():
            local_team = row['Equipo_local']
            visit_team = row['Equipo_visitante']
            local_goals = row['Goles_local']
            visit_goals = row['Goles_visitante']

            if local_goals > visit_goals:
                self.update_table(local_team, 3, local_goals, visit_goals, table_positions)
                self.update_table(visit_team, 0, visit_goals, local_goals, table_positions)
            elif local_goals < visit_goals:
                self.update_table(local_team, 0, local_goals, visit_goals, table_positions)
                self.update_table(visit_team, 3, visit_goals, local_goals, table_positions)
            else:
                self.update_table(local_team, 1, local_goals, visit_goals, table_positions)
                self.update_table(visit_team, 1, visit_goals, local_goals, table_positions)

            local_scorers = self.get_scorers(row['Goleadores_local'])
            visit_scorers = self.get_scorers(row['Goleadores_visitante'])
            self.update_scorers(local_scorers, table_scorers)
            self.update_scorers(visit_scorers, table_scorers)

        # Ordenar tabla de posiciones por puntos (de mayor a menor)
        sorted_positions = dict(sorted(table_positions.items(), key=lambda item: item[1]['Puntos'], reverse=True))

        # Ordenar tabla de goleadores por goles (de mayor a menor)
        sorted_scorers = dict(sorted(table_scorers.items(), key=lambda item: item[1], reverse=True))

        # Generar imágenes
        self.generate_image("Tabla de Posiciones", sorted_positions, "posiciones.png")
        self.generate_image("Tabla de Goleadores", sorted_scorers, "goleadores.png")

        messagebox.showinfo("Éxito", "Tablas generadas y guardadas como imágenes")

    def get_scorers(self, scorers_cell):
        if pd.isna(scorers_cell):
            return []
        return scorers_cell.split(',')

    def update_table(self, team, points, goals_for, goals_against, table):
        if team not in table:
            table[team] = {'Puntos': 0, 'Goles a favor': 0, 'Goles en contra': 0, 'Partidos': 0}
        
        table[team]['Puntos'] += points
        table[team]['Goles a favor'] += goals_for
        table[team]['Goles en contra'] += goals_against
        table[team]['Partidos'] += 1

    def update_scorers(self, scorers, table_scorers):
        for scorer in scorers:
            scorer = scorer.strip()
            if scorer:
                if scorer not in table_scorers:
                    table_scorers[scorer] = 0
                table_scorers[scorer] += 1

    def generate_image(self, title, table, filename):
        fig, ax = plt.subplots()

        if title == "Tabla de Posiciones":
            data = [(team, stats['Puntos'], stats['Goles a favor'], stats['Goles en contra'], stats['Partidos']) for team, stats in table.items()]
            columns = ["Equipo", "Puntos", "Goles a favor", "Goles en contra", "Partidos"]
        else:
            data = [(scorer, goals) for scorer, goals in table.items()]
            columns = ["Goleador", "Goles"]

        # Crear tabla visual con matplotlib
        ax.axis('tight')
        ax.axis('off')
        ax.table(cellText=data, colLabels=columns, cellLoc='center', loc='center')

        # Guardar la imagen
        plt.title(title, fontsize=16)
        plt.savefig(filename, bbox_inches='tight')
        plt.close()

        self.status_label.config(text=f"Imágenes guardadas: posiciones.png, goleadores.png")

if __name__ == "__main__":
    root = tk.Tk()
    app = FootballApp(root)
    root.mainloop()



