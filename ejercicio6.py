from datetime import date

from billetera import Billetera
from categoria import Categoria
from movimiento import Gasto, Ingreso
from usuario import Usuario

edwin = Usuario(1, "Edwin")
novia = Usuario(2, "Novia")
comida = Categoria("Comida", "🍔")
transporte = Categoria("Transporte", "🚗")
trabajo = Categoria("Trabajo", "💼")
billetera = Billetera("Gastos de la casa")


def mostrar(llamada, movimientos):
    print(f"{llamada} -> {len(movimientos)} movimiento(s)")
    for movimiento in movimientos:
        print("    ", movimiento.resumen())


print("=== registrar(*movimientos): uno o varios en la misma llamada ===")
billetera.registrar(Ingreso(1, "600", edwin, trabajo, "Quincena", date(2026, 10, 15)))
print("Con un argumento:   ", len(billetera), "movimiento")
billetera.registrar(
    Gasto(2, "12.50", novia, comida, "Pizza", date(2026, 10, 15), "Tarjeta"),
    Gasto(3, "3.25", edwin, transporte, "Bus", date(2026, 10, 16)),
    Gasto(4, "18", edwin, comida, "Supermercado", date(2026, 9, 28), "Tarjeta"),
)
print("Con tres argumentos:", len(billetera), "movimientos")

print("\n=== filtrar(tipo=None, **criterios): un método, varias formas ===")
mostrar("filtrar()", billetera.filtrar())
mostrar("filtrar(Gasto)", billetera.filtrar(Gasto))
mostrar(
    'filtrar(Gasto, categoria="comida")', billetera.filtrar(Gasto, categoria="comida")
)
mostrar('filtrar(mes=10, usuario="Edwin")', billetera.filtrar(mes=10, usuario="Edwin"))

print("\n=== Llamadas que no corresponden a ninguna versión ===")
try:
    billetera.filtrar(color="rojo")
except TypeError as error:
    print('filtrar(color="rojo") ->', error)
try:
    billetera.registrar()
except TypeError as error:
    print("registrar() ->", error)
