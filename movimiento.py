"""Movimientos de dinero: clase abstracta Movimiento y sus cuatro subclases.

Son los mismos cuatro tipos de la app: Gasto, Ingreso, Ahorro y Retiro.
"""

from abc import ABC, abstractmethod
from datetime import date
from decimal import Decimal, InvalidOperation

from categoria import Categoria
from excepciones import CategoriaNoPermitidaError
from usuario import Usuario

CENTAVO = Decimal("0.01")
FORMATO_FECHA = "%d/%m/%Y"
METODOS_PAGO = ("Efectivo", "Tarjeta", "Transferencia", "Otro")


class Movimiento(ABC):
    """Clase abstracta con lo que comparte cualquier movimiento de dinero.

    No se puede instanciar: obliga a cada subclase a definir efecto_en_balance().
    Reemplaza el atributo tipo y los if de las versiones anteriores.
    """

    TIPO = None  # cada subclase pone el suyo

    def __init__(
        self,
        id_mov,
        monto,
        usuario,
        categoria,
        descripcion="",
        fecha=None,
        metodo_pago="Efectivo",
    ):
        if not isinstance(usuario, Usuario):
            raise TypeError("usuario debe ser un objeto Usuario")
        if not isinstance(categoria, Categoria):
            raise TypeError("categoria debe ser un objeto Categoria")
        if not categoria.permite(self.TIPO):
            raise CategoriaNoPermitidaError(categoria.nombre, self.TIPO)
        if metodo_pago not in METODOS_PAGO:
            raise ValueError(f"Método de pago no válido: {metodo_pago}")
        self.__id = id_mov  # int (primitivo), solo lectura
        self.monto = monto  # Decimal (tipo clase), validado por el setter
        self.usuario = usuario  # Usuario (tipo clase)
        self.categoria = categoria  # Categoria (tipo clase)
        self.descripcion = descripcion  # str (primitivo)
        self.fecha = fecha or date.today()  # date (tipo clase)
        self.metodo_pago = metodo_pago  # str (primitivo)

    @property
    def id(self):
        return self.__id

    @property
    def monto(self):
        return self._monto

    @monto.setter
    def monto(self, valor):
        if not self.es_monto_valido(valor):
            raise ValueError(f"Monto no válido: {valor}")
        self._monto = Decimal(str(valor)).quantize(CENTAVO)

    @abstractmethod
    def efecto_en_balance(self):
        """Cada subclase decide si suma o resta al balance disponible."""

    def resumen(self):
        """Devuelve el movimiento en una línea, como en la lista de la app."""
        fecha_texto = self.fecha.strftime(FORMATO_FECHA)
        etiqueta = f"{self.categoria.emoji} {self.descripcion or self.categoria.nombre}"
        return (
            f"{fecha_texto}  {self.TIPO:<8} {self.efecto_en_balance():+9,.2f}  "
            f"{etiqueta} · {self.usuario.nombre}"
        )

    @staticmethod
    def es_monto_valido(monto):
        """Regla del gestor: el monto es mayor que cero y tiene máximo dos decimales."""
        if isinstance(monto, bool):
            return False
        try:
            valor = Decimal(str(monto))
            return valor.is_finite() and valor > 0 and valor == valor.quantize(CENTAVO)
        except InvalidOperation:
            return False

    def __eq__(self, otro):
        if not isinstance(otro, Movimiento):
            return NotImplemented
        return self.__id == otro.__id

    def __hash__(self):
        return hash(self.__id)


class Gasto(Movimiento):
    """Dinero que sale: resta al balance."""

    TIPO = "Gasto"

    def efecto_en_balance(self):
        return -self._monto


class Ingreso(Movimiento):
    """Dinero que entra, con el periodo que cubre (ej. "1-15 oct")."""

    TIPO = "Ingreso"

    def __init__(
        self,
        id_mov,
        monto,
        usuario,
        categoria,
        descripcion="",
        fecha=None,
        metodo_pago="Transferencia",
        periodo="",
    ):
        super().__init__(
            id_mov, monto, usuario, categoria, descripcion, fecha, metodo_pago
        )
        self.periodo = periodo  # str (primitivo)

    def efecto_en_balance(self):
        return self._monto

    def resumen(self):
        texto = super().resumen()
        return f"{texto}  ({self.periodo})" if self.periodo else texto


class Ahorro(Movimiento):
    """Dinero que pasa del balance disponible al pote de ahorros."""

    TIPO = "Ahorro"

    def efecto_en_balance(self):
        return -self._monto


class Retiro(Movimiento):
    """Dinero que regresa del pote de ahorros al balance disponible."""

    TIPO = "Retiro"

    def efecto_en_balance(self):
        return self._monto
