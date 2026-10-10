"""Billetera compartida: agrupa movimientos y contiene su propio pote de ahorros."""

from decimal import Decimal

from movimiento import Ahorro, Movimiento, Retiro
from pote_ahorro import PoteDeAhorro

# Filtros que acepta filtrar() por nombre
CRITERIOS_VALIDOS = {"categoria", "mes", "usuario", "metodo_pago"}


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

    # SOBRECARGA SIMULADA 1: registrar(*movimientos)
    # En Java habría que escribir registrar(Movimiento m) y registrar(Movimiento... ms).
    # En Python, *movimientos junta todos los argumentos en una tupla, así que el mismo
    # método acepta registrar(m1) o registrar(m1, m2, m3). Se registran en orden: si
    # uno falla, los anteriores ya quedaron guardados, igual que con llamadas sueltas.
    def registrar(self, *movimientos):
        """Agrega uno o varios movimientos; ahorros y retiros pasan por el pote."""
        if not movimientos:
            raise TypeError("registrar() necesita al menos un movimiento")
        for movimiento in movimientos:
            if not isinstance(movimiento, Movimiento):
                raise TypeError("Solo se pueden registrar objetos Movimiento")
            if isinstance(movimiento, Ahorro):
                self.__pote.depositar(movimiento.monto)
            elif isinstance(movimiento, Retiro):
                self.__pote.retirar(movimiento.monto)  # puede lanzar un error
            self.__movimientos.append(movimiento)

    # SOBRECARGA SIMULADA 2: filtrar(tipo=None, **criterios)
    # En Java serían varios métodos con el mismo nombre y distintos parámetros:
    #   filtrar(), filtrar(Class tipo), filtrar(Class tipo, String categoria),
    #   filtrar(int mes, String usuario)...
    # Aquí uno solo cubre todas las combinaciones: tipo tiene un valor por defecto y
    # **criterios recibe cualquier filtro por nombre, como los filtros de mes y
    # categoría del Resumen de la app o el de usuario de la pestaña Usuarios.
    def filtrar(self, tipo=None, **criterios):
        """Devuelve los movimientos del tipo y con los criterios indicados."""
        desconocidos = set(criterios) - CRITERIOS_VALIDOS
        if desconocidos:
            raise TypeError(f"Criterio no válido: {', '.join(sorted(desconocidos))}")
        return [
            movimiento
            for movimiento in self.__movimientos
            if (tipo is None or isinstance(movimiento, tipo))
            and self._cumple_criterios(movimiento, criterios)
        ]

    @staticmethod
    def _cumple_criterios(movimiento, criterios):
        valores = {
            "mes": movimiento.fecha.month,
            "categoria": movimiento.categoria.nombre.lower(),
            "usuario": movimiento.usuario.nombre.lower(),
            "metodo_pago": movimiento.metodo_pago.lower(),
        }
        return all(
            valores[clave]
            == (esperado.lower() if isinstance(esperado, str) else esperado)
            for clave, esperado in criterios.items()
        )

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
