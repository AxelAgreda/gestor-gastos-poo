from datetime import date
from decimal import Decimal

from act1_movimiento import Movimiento as MovimientoConFloat
from ej1_movimiento import Movimiento as MovimientoConDecimal

MovimientoConFloat.REGISTRAR_CICLO = False  # apago los mensajes de la Actividad 1

print("=== El problema: float guarda 0.1 de forma aproximada ===")
print("0.1 + 0.2 =", 0.1 + 0.2)
print("Decimal('0.1') + Decimal('0.2') =", Decimal("0.1") + Decimal("0.2"))


def balance_de_diez_cafes(clase_movimiento):
    """Registra diez gastos de $0.10 y devuelve el balance."""
    cafes = [
        clase_movimiento(numero, "Gasto", 0.10, "Comida", "Café", date(2026, 10, 9))
        for numero in range(1, 11)
    ]
    balance = 0
    for cafe in cafes:  # acumulo uno por uno, como lo hace la app al registrar
        balance += cafe.efecto_en_balance()
    return balance


print("\n=== Diez gastos de $0.10 ===")
balance_antes = balance_de_diez_cafes(MovimientoConFloat)
balance_despues = balance_de_diez_cafes(MovimientoConDecimal)
print("ANTES   (float):  ", repr(balance_antes), "| ¿es -1?", balance_antes == -1)
print("DESPUÉS (Decimal):", repr(balance_despues), "| ¿es -1?", balance_despues == -1)

print("\n=== La validación sigue funcionando ===")
recibo = MovimientoConDecimal(11, "Gasto", "45", "Casa", "Internet", date(2026, 10, 9))
print("Monto '45' guardado como:", repr(recibo.monto))
print("Historial:", recibo.resumen())
for monto in ("12.345", "-5", "abc"):
    print(f"es_monto_valido({monto!r}) ->", MovimientoConDecimal.es_monto_valido(monto))
