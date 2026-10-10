"""Pote de ahorros: el dinero apartado con movimientos de tipo Ahorro."""

from decimal import Decimal

from excepciones import AhorroInsuficienteError


class PoteDeAhorro:
    """Lleva el ahorro acumulado. Es parte de una Billetera y no existe sin ella."""

    def __init__(self):
        self.__saldo = Decimal("0.00")

    @property
    def saldo(self):
        return self.__saldo

    def depositar(self, monto):
        self.__saldo += monto

    def retirar(self, monto):
        """Saca dinero del ahorro. No permite dejar el saldo en negativo."""
        if monto > self.__saldo:
            raise AhorroInsuficienteError(monto, self.__saldo)
        self.__saldo -= monto
