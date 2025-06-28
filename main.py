# importar librerias y logica
import tkinter as tk
from gui import descargadorGUI 


if __name__ == "__main__":
# crear ventana principal
    root = tk.Tk()
# indicar clase desde gui.py
    app = descargadorGUI(root)
# bucle de tkinker
    root.mainloop()