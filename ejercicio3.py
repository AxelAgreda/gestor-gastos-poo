from ej3_movimiento import Ingreso, Movimiento

# Prueba de regresión: después de reorganizar desde_texto() en funciones más
# cortas, el resultado tiene que ser el mismo que antes.
linea = "5; gasto; $1,250.75; casa; Alquiler; 09/10/2026"
alquiler = Movimiento.desde_texto(linea)
print("Línea original:", linea)
print("Objeto creado: ", alquiler.resumen())

try:
    Movimiento.desde_texto("6;Gasto;20;Comida")
except ValueError as error:
    print("Línea incompleta ->", error)

quincena = Ingreso(7, "600", "trabajo", "Quincena", alquiler.fecha, "16-31 oct")
print(quincena.resumen())
