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

            # Calcular goleadores (asume que los goleadores están separados por comas)
            local_scorers = row['Goleadores_local'].split(',')
            visit_scorers = row['Goleadores_visitante'].split(',')
            self.update_scorers(local_scorers, table_scorers)
            self.update_scorers(visit_scorers, table_scorers)

        # Mostrar tablas
        self.show_tables(table_positions, table_scorers)

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

    def show_tables(self, table_positions, table_scorers):
        print("Tabla de posiciones:")
        for team, stats in sorted(table_positions.items(), key=lambda x: (-x[1]['Puntos'], -x[1]['Goles a favor'])):
            print(f"{team}: {stats['Puntos']} puntos, {stats['Goles a favor']} GF, {stats['Goles en contra']} GC, {stats['Partidos']} PJ")
        
        print("\nTabla de goleadores:")
        for scorer, goals in sorted(table_scorers.items(), key=lambda x: -x[1]):
            print(f"{scorer}: {goals} goles")

if __name__ == "__main__":
    root = tk.Tk()
    app = FootballApp(root)
    root.mainloop()
