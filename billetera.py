"""Billetera compartida: agrupa movimientos y contiene su propio pote de ahorros."""

from decimal import Decimal

from movimiento import Ahorro, Movimiento, Retiro
from pote_ahorro import PoteDeAhorro


class Billetera:
    """Reúne los movimientos de los usuarios que comparten la app."""

    def __init__(self, nombre):
        self.nombre = nombre  # str (primitivo)
        # AGRUPACIÓN: la billetera guarda una lista de movimientos que se crean
        # afuera y pueden seguir existiendo aunque la billetera desaparezca.
        self.__movimientos = []
        # COMPOSICIÓN: el pote se crea aquí adentro, no se recibe de afuera y
        # nadie más tiene una referencia a él. Vive y muere con la billetera.
        self.__pote = PoteDeAhorro()

    def registrar(self, movimiento):
        """Agrega un movimiento. Los ahorros y retiros pasan por el pote."""
        if not isinstance(movimiento, Movimiento):
            raise TypeError("Solo se pueden registrar objetos Movimiento")
        if isinstance(movimiento, Ahorro):
            self.__pote.depositar(movimiento.monto)
        elif isinstance(movimiento, Retiro):
            self.__pote.retirar(movimiento.monto)  # puede lanzar un error
        self.__movimientos.append(movimiento)

    @property
    def movimientos(self):
        """Copia de solo lectura: desde afuera no se puede agregar sin registrar()."""
        return tuple(self.__movimientos)

    @property
    def ahorro_acumulado(self):
        return self.__pote.saldo

    def balance(self):
        """Ingresos - Gastos - (Ahorros - Retiros), la misma fórmula de la app."""
        return sum(
            (movimiento.efecto_en_balance() for movimiento in self.__movimientos),
            Decimal("0.00"),
        )

    def __len__(self):
        return len(self.__movimientos)
