import tkinter
import PIL
import sqlite3
import pandas as pd
import plotly
import os
import sys

print("Tkinter version:", tkinter.TkVersion)
print("Pillow (PIL) version:", PIL.__version__)
print("SQLite version:", sqlite3.sqlite_version)
print("Pandas version:", pd.__version__)
print("Plotly version:", plotly.__version__)
print("OS version:", os.name)
print("Python version:", sys.version)
