# gui_elements.py

import tkinter as tk
from tkinter import messagebox, ttk
import threading

# importar logica del descargador
import descargador_gui

class descargadorGUI:
    def __init__(self, master):
        self.master = master
        master.title("el super descargador bro")
        master.geometry("500x380")
        master.resizable(False, False)

        # logica de los widgets
        self.url_var = tk.StringVar()
        self.format_var = tk.StringVar(value="video")
        self.use_threading_var = tk.BooleanVar(value=True)

        # titulo
        tk.Label(master, text="Descargador de mp3 y mp4", font=("Arial", 16, "bold")).pack(pady=10)

        # campo de la url
        tk.Label(master, text="ingresa la url de YouTube a descargar:").pack(anchor='w', padx=50)
        self.url_entry = tk.Entry(master, textvariable=self.url_var, width=60)
        self.url_entry.pack(pady=5, padx=50)

        # opciones de formato
        tk.Label(master, text="escoge el formato que quieres:").pack(anchor='w', padx=50)
        tk.Radiobutton(master, text="Video (MP4)", variable=self.format_var, value="video").pack(anchor='w', padx=60)
        tk.Radiobutton(master, text="Audio (MP3)", variable=self.format_var, value="audio").pack(anchor='w', padx=60)

        # opcion de threading para no congelar la interfaz
        self.threading_checkbox = tk.Checkbutton(master,
                                                 text="descargar en segundo plano (recomendado)",
                                                 variable=self.use_threading_var)
        self.threading_checkbox.pack(anchor='w', padx=50, pady=10)

        # boton de descarga
        self.download_button = tk.Button(master, text="descargar...", command=self.on_download_click,
                                         font=("Arial", 12, "bold"), bg="#006aff", fg="white")
        self.download_button.pack(pady=5)

        # barra de progreso
        self.progress_bar = ttk.Progressbar(master, orient="horizontal", length=380, mode="determinate")
        self.progress_bar.pack(pady=5)
                                        
        # eiqueta de estado
        self.status_label = tk.Label(master, text="listo para descargar...", wraplength=450)
        self.status_label.pack(pady=5)

    # actualizar la GUI desde el hilo de descarga
    def update_gui_elements_from_thread(self, percent, message):
        self.master.after(0, lambda: self._actualizar_widgets_directamente(percent, message))

    # actualiza los widgets de la gui
    def _actualizar_widgets_directamente(self, percent, message):
        self.progress_bar['value'] = percent
        self.status_label.config(text=message)
        self.master.update_idletasks() 

    # solicitar y verificar si la url esta biem
    def on_download_click(self):
        url = self.url_var.get().strip()
        format_choice = self.format_var.get()
        use_threading = self.use_threading_var.get()

        if not url:
            messagebox.showwarning("Ey", "por favor, ingresa una url de youtube válida.")
            return

        self.download_button.config(state=tk.DISABLED)
        self.progress_bar['value'] = 0
        self.status_label.config(text="preparando descarga, espera....")

        # logica para el threading
        if use_threading:
            self.status_label.config(text="iniciando descarga en segundo plano...")
            threading.Thread(target=self._start_download_thread_target,
                             args=(url, format_choice)).start()
        else:
            self.status_label.config(text="iniciando descarga (puede que la interfaz se congele)...")
            self._start_download_thread_target(url, format_choice)

    #logica de descarga
    def _start_download_thread_target(self, url, format_choice):
        success, result_message = descargador_gui.start_download_process(
            url, format_choice, self.update_gui_elements_from_thread
        )
        # actualizar el resultaod
        self.master.after(0, lambda: self._handle_download_result(success, result_message))

    # manejar el resultado final
    def _handle_download_result(self, success, message):
        if success:
            messagebox.showinfo("Éxito", f"Descarga finalizada, se descargo: '{message}'")
            self.status_label.config(text=f"Descarga finalizada: {message}")
            self.progress_bar['value'] = 100
        else:
            messagebox.showerror("Error", f"fallo en la descarga: {message}")
            self.status_label.config(text=f"error (vete a saber cual): {message}")
            self.progress_bar['value'] = 0

        self.download_button.config(state=tk.NORMAL) 