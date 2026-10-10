"""Errores propios del gestor de gastos."""


class GestorGastosError(Exception):
    """Base para todos los errores esperados del proyecto."""


class CategoriaNoPermitidaError(GestorGastosError):
    """La categoría no está habilitada para ese tipo de movimiento.

    En la app, cada categoría tiene una columna Tipos que dice en qué
    formularios aparece (Gasto, Ingreso, Ahorro, Retiro).
    """

    def __init__(self, categoria, tipo):
        self.categoria = categoria
        self.tipo = tipo
        super().__init__(f"La categoría {categoria} no está habilitada para {tipo}")


class AhorroInsuficienteError(GestorGastosError):
    """Se intenta retirar del ahorro más de lo que hay acumulado."""

    def __init__(self, solicitado, disponible):
        self.solicitado = solicitado
        self.disponible = disponible
        super().__init__(
            f"Quieres retirar ${solicitado:,.2f} y el ahorro acumulado es "
            f"${disponible:,.2f}"
        )
