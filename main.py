import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
from openpyxl import load_workbook

class FootballApp:
    def __init__(self, root):
        self.root = root