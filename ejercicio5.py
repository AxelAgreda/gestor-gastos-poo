from datetime import date

from billetera import Billetera
from categoria import Categoria
from excepciones import AhorroInsuficienteError, CategoriaNoPermitidaError
from movimiento import Ahorro, Gasto, Ingreso, Movimiento, Retiro
from usuario import Usuario

edwin = Usuario(1, "Edwin")
novia = Usuario(2, "Novia")
comida = Categoria("Comida", "🍔", tipos=["Gasto"])
trabajo = Categoria("Trabajo", "💼", tipos=["Gasto", "Ingreso"])
fondo = Categoria("Fondo de emergencia", "🏦", tipos=["Ahorro", "Retiro"])

# Este ahorro se crea afuera de la billetera (importa para el punto d)
ahorro_quincena = Ahorro(
    3, "100", edwin, fondo, "Ahorro de quincena", date(2026, 10, 15)
)

billetera = Billetera("Gastos de la casa")
billetera.registrar(
    Ingreso(
        1, "600", edwin, trabajo, "Quincena", date(2026, 10, 15), periodo="1-15 oct"
    )
)
billetera.registrar(
    Gasto(2, "12.50", novia, comida, "Pizza", date(2026, 10, 15), metodo_pago="Tarjeta")
)
billetera.registrar(ahorro_quincena)
billetera.registrar(Retiro(4, "30", novia, fondo, "Emergencia", date(2026, 10, 20)))

print("=== (a) Variables primitivas y de tipo clase en un mismo objeto ===")
pizza = billetera.movimientos[1]
for atributo in ("id", "metodo_pago", "monto", "fecha", "usuario", "categoria"):
    valor = getattr(pizza, atributo)
    print(f"  {atributo:<12} {type(valor).__name__:<10} {valor!r}")

print("\n=== (b) Clase abstracta ===")
try:
    Movimiento(99, "10", edwin, comida)
except TypeError as error:
    print("Movimiento(...) ->", error)
for clase in (Gasto, Ingreso, Ahorro, Retiro):
    print(f"  {clase.__name__:<8} hereda de {clase.__bases__[0].__name__}")

print("\n=== (c) Composición: el pote de ahorros vive dentro de la billetera ===")
print(f"Ahorro acumulado: ${billetera.ahorro_acumulado:,.2f}")
try:
    billetera.registrar(Retiro(5, "200", edwin, fondo, "Viaje", date(2026, 10, 25)))
except AhorroInsuficienteError as error:
    print("Retiro rechazado:", error)
try:
    Gasto(6, "8", edwin, fondo, "Café")
except CategoriaNoPermitidaError as error:
    print("Gasto rechazado:", error)

print("\n=== (d) Agrupación: la billetera reúne varios movimientos ===")
for movimiento in billetera.movimientos:
    print("  ", movimiento.resumen())
print(f"Movimientos: {len(billetera)} | Balance: ${billetera.balance():,.2f}")
print("(600 de ingreso - 12.50 de gasto - 100 de ahorro + 30 de retiro)")

del billetera
print("Después de borrar la billetera, el ahorro registrado sigue existiendo:")
print("  ", ahorro_quincena.resumen())
