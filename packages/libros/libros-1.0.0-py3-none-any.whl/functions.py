import pandas as pd
import tkinter as tk
from tkinter import messagebox

class LibroFinder:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title('Buscador de Libros')

        self.etiqueta_instruccion = tk.Label(self.ventana, text='Ingrese el ISBN del libro:')
        self.etiqueta_instruccion.pack()

        self.entrada_isbn = tk.Entry(self.ventana)
        self.entrada_isbn.pack()

        self.boton_buscar = tk.Button(self.ventana, text='Buscar', command=self.buscar_libro2)
        self.boton_buscar.pack()

    def buscar_libro1(self, isbn):
        try:
            datos = pd.read_csv('libros.csv', delimiter=';')
            libro = datos.loc[datos['ISBN'] == isbn]

            if not libro.empty:
                messagebox.showinfo('Datos del Libro', str(libro))
            else:
                messagebox.showerror('Error', 'No se encontró el libro')
        except FileNotFoundError:
            messagebox.showerror('Error', 'No se encontró el archivo CSV')

    def buscar_libro2(self):
        isbn = self.entrada_isbn.get()
        self.buscar_libro1(isbn)

    def run(self):
        self.ventana.mainloop()

if __name__ == '__main__':
    buscador = LibroFinder()
    buscador.run()
