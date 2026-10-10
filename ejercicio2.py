from datetime import date

from ej2_movimiento import Ingreso, Movimiento

historial = [
    Movimiento(1, "Gasto", "12.50", "Comida", "Almuerzo", date(2026, 10, 14)),
    Movimiento(2, "Gasto", "3.25", "Transporte", "Bus", date(2026, 10, 14)),
    Ingreso(3, "600", "Trabajo", "Quincena", date(2026, 10, 15), periodo="1-15 oct"),
    Ingreso(4, "45", "Otros", "Venta de audífonos", date(2026, 10, 16)),
]

print("=== Polimorfismo: el mismo llamado, distinta respuesta ===")
for movimiento in historial:
    print(f"{type(movimiento).__name__:<11} {movimiento.resumen()}")

print("\n=== Herencia: Ingreso reutiliza lo del padre ===")
quincena = historial[2]
print("¿quincena es un Movimiento?", isinstance(quincena, Movimiento))
print("Tipo (heredado, fijado por la subclase):", quincena.tipo)
print("Efecto en el balance (heredado):", quincena.efecto_en_balance())
print("Periodo (atributo propio):", quincena.periodo)

balance = sum(movimiento.efecto_en_balance() for movimiento in historial)
print(f"\nBalance del periodo: ${balance:,.2f}")
