import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from openpyxl import load_workbook
import matplotlib.pyplot as plt
from PIL import Image, ImageTk, ImageOps
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
        
        self.select_image_button = ttk.Button(self.root, text="Seleccionar imagen de fondo", command=self.select_background_image)
        self.select_image_button.pack(pady=10)
        
        self.generate_button = ttk.Button(self.root, text="Generar tablas e imágenes", command=self.generate_table)
        self.generate_button.pack(pady=10)

        self.status_label = ttk.Label(self.root, text="")
        self.status_label.pack(pady=20)
        
        self.file_path = None
        self.background_image = None  # Para almacenar la imagen de fondo
        self.data = None

    def upload_file(self):
        self.file_path = filedialog.askopenfilename(title="Selecciona el archivo Excel", filetypes=[("Excel files", "*.xlsx")])
        if self.file_path:
            self.data = pd.read_excel(self.file_path)
            messagebox.showinfo("Cargado", "Archivo cargado correctamente")
            self.status_label.config(text="Archivo cargado: " + os.path.basename(self.file_path))

    def select_background_image(self):
        image_path = filedialog.askopenfilename(title="Selecciona una imagen de fondo", filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if image_path:
            self.background_image = Image.open(image_path)
            messagebox.showinfo("Imagen cargada", "Imagen de fondo seleccionada correctamente")
            self.status_label.config(text="Imagen seleccionada: " + os.path.basename(image_path))

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
            # Línea 77:
            self.update_scorers(local_scorers, table_scorers)

            # Línea 78:
            self.update_scorers(visit_scorers, table_scorers)

        # Ordenar tabla de posiciones por puntos (de mayor a menor)
        sorted_positions = dict(sorted(table_positions.items(), key=lambda item: item[1]['Puntos'], reverse=True))

        # Ordenar tabla de goleadores por goles (de mayor a menor)
        sorted_scorers = dict(sorted(table_scorers.items(), key=lambda item: item[1], reverse=True))

        # Generar imágenes optimizadas para móvil
        self.generate_image("Tabla de Posiciones", sorted_positions, "posiciones_movil.png", mobile=True)
        self.generate_image("Tabla de Goleadores", sorted_scorers, "goleadores_movil.png", mobile=True)

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

    def generate_image(self, title, table, filename, mobile=False):
        # Ajustar el tamaño de la imagen dependiendo de si es para móvil o no
        if mobile:
            fig_width, fig_height = 6, 10  # Dimensiones optimizadas para pantalla de móvil (720x1280 px aproximadamente)
            dpi = 150  # DPI adecuado para alta calidad en móviles
        else:
            fig_width, fig_height = 10, 8  # Tamaño estándar
            dpi = 300  # Alta resolución para pantallas grandes

        fig, ax = plt.subplots(figsize=(fig_width, fig_height), dpi=dpi)

        if title == "Tabla de Posiciones":
            data = [(team, stats['Puntos'], stats['Goles a favor'], stats['Goles en contra'], stats['Partidos']) for team, stats in table.items()]
            columns = ["Equipo", "Puntos", "Goles a favor", "Goles en contra", "Partidos"]
        else:
            data = [(scorer, goals) for scorer, goals in table.items()]
            columns = ["Goleador", "Goles"]

        # Si hay una imagen de fondo seleccionada, ponerla en el fondo de la tabla
        if self.background_image:
            # Convertir la imagen de fondo para que coincida con el tamaño de la figura
            fig_width_px, fig_height_px = fig.get_size_inches() * fig.dpi
            bg_image_resized = self.background_image.resize((int(fig_width_px), int(fig_height_px)))
            ax.imshow(bg_image_resized, extent=[0, 1, 0, 1], aspect='auto', zorder=-1)  # Colocar imagen de fondo

        # Crear tabla visual con matplotlib
        ax.axis('tight')
        ax.axis('off')

        # Calcular el ancho máximo de cada columna
        column_widths = [max(len(str(item)) for item in [col] + [row[i] for row in data]) for i, col in enumerate(columns)]
        # Ajustar el tamaño de las columnas
        cell_widths = [width * 0.2 for width in column_widths]  # Ajustar el factor según la visualización deseada

        # Establecer el alto de las filas
        cell_height = 0.5  # Ajustar según sea necesario

        table = ax.table(cellText=data, colLabels=columns, cellLoc='center', loc='center')
        
        # Ajustar el ancho y alto de cada celda
        for i, width in enumerate(cell_widths):
            table.auto_set_column_width(i)
            table[i, 0].set_width(width * 0.1)  # Ajustar ancho (0.1 es un factor que puedes modificar)

        for i in range(len(data)):
            table[(i + 1, 0)].set_height(cell_height)  # Establecer alto para cada fila

        plt.title(title, fontsize=16)
        plt.savefig(filename, bbox_inches='tight', dpi=dpi)
        plt.close()

        self.status_label.config(text=f"Imágenes guardadas: {filename}")


if __name__ == "__main__":
    root = tk.Tk()
    app = FootballApp(root)
    root.mainloop()





