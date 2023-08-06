import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class GraficasApp:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title('Aplicación de Gráficas')

        # Crear los botones de las opciones
        self.btn_barras = tk.Button(self.ventana, text='Gráfica de Barras', command=self.mostrar_grafica_barras)
        self.btn_barras.pack()

        self.btn_lineal = tk.Button(self.ventana, text='Gráfica Lineal', command=self.mostrar_grafica_lineal)
        self.btn_lineal.pack()

        self.btn_pastel = tk.Button(self.ventana, text='Gráfica de Pastel', command=self.mostrar_grafica_pastel)
        self.btn_pastel.pack()

        # Crear el lienzo para mostrar las gráficas
        self.lienzo = tk.Canvas(self.ventana, width=600, height=400)
        self.lienzo.pack()

        # Variable para almacenar la referencia a la figura actual
        self.figura_actual = None

    def mostrar_grafica_barras(self):
        # Cerrar la figura anterior
        self.cerrar_figura_actual()

        # Datos para la gráfica de barras
        paises = ['Estados Unidos', 'China', 'Japón', 'Alemania', 'India', 'Reino Unido', 'Francia', 'Italia', 'Canadá', 'Brasil',
                  'Rusia', 'Corea', 'Australia', 'México', 'España', 'Indonesia', 'Países Bajos', 'Arabia Saudita', 'Turquía', 'Suiza']
        riqueza = [26.85460, 19.37359, 4.40974, 4.30885, 3.73688, 3.15894, 2.92349, 2.16975, 2.08967, 2.08124,
                   2.06265, 1.72191, 1.70755, 1.66316, 1.49243, 1.39178, 1.08088, 1.06190, 1.02930, 0.86960]

        # Graficar la gráfica de barras en el lienzo
        figura = plt.figure(figsize=(6, 4))
        plt.bar(range(len(paises)), riqueza, tick_label=paises)
        plt.xlabel('País')
        plt.ylabel('Riqueza (billones)')
        plt.title('Riqueza de los países')
        plt.xticks(rotation=90)
        plt.tight_layout()

        # Mostrar la figura en el lienzo
        self.mostrar_en_lienzo(figura)

    def mostrar_grafica_lineal(self):
        # Cerrar la figura anterior
        self.cerrar_figura_actual()

        # Datos para la gráfica lineal
        periodo = [1990, 1995, 2000, 2005, 2010, 2015, 2020]
        indice_envejecimiento = [16.0, 18.5, 21.3, 26.4, 30.9, 38.0, 47.7]

        # Graficar la gráfica lineal en el lienzo
        figura = plt.figure(figsize=(6, 4))
        plt.plot(periodo, indice_envejecimiento, marker='o')
        plt.xlabel('Periodo')
        plt.ylabel('Porcentaje')
        plt.title('Índice de Envejecimiento')
        plt.tight_layout()

        # Mostrar la figura en el lienzo
        self.mostrar_en_lienzo(figura)

    def mostrar_grafica_pastel(self):
        # Cerrar la figura anterior
        self.cerrar_figura_actual()

        # Datos para la gráfica de pastel
        defunciones = [10774, 8450]
        etiquetas = ['Hombres', 'Mujeres']

        # Graficar la gráfica de pastel en el lienzo
        figura = plt.figure(figsize=(4, 4))
        plt.pie(defunciones, labels=etiquetas, autopct='%1.1f%%', startangle=90)
        plt.title('Defunciones menores de un año')
        plt.axis('equal')
        plt.tight_layout()

        # Mostrar la figura en el lienzo
        self.mostrar_en_lienzo(figura)

    def mostrar_en_lienzo(self, figura):
        # Limpiar el lienzo antes de mostrar la nueva gráfica
        self.lienzo.delete('all')

        # Convertir la figura de matplotlib en una imagen que se puede mostrar en el lienzo
        figura_canvas = FigureCanvasTkAgg(figura, master=self.lienzo)
        figura_canvas.draw()

        # Almacenar la referencia a la figura actual
        self.figura_actual = figura

        # Agregar la figura_canvas al lienzo
        figura_canvas.get_tk_widget().pack()

    def cerrar_figura_actual(self):
        if self.figura_actual is not None:
            plt.close(self.figura_actual)
            self.figura_actual = None

    def run(self):
        self.ventana.mainloop()

# Programa principal
if __name__ == '__main__':
    app = GraficasApp()
    app.run()
