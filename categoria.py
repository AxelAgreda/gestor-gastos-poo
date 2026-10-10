"""Categorías de movimiento, como en la hoja Categorias de la app."""

TIPOS_MOVIMIENTO = ("Gasto", "Ingreso", "Ahorro", "Retiro")


class Categoria:
    """Categoría con emoji y los tipos de movimiento en los que aparece."""

    def __init__(self, nombre, emoji="💰", tipos=TIPOS_MOVIMIENTO):
        nombre_limpio = " ".join(str(nombre).split()).capitalize()
        if not nombre_limpio:
            raise ValueError("La categoría necesita un nombre")
        tipos_validos = {tipo for tipo in tipos if tipo in TIPOS_MOVIMIENTO}
        if not tipos_validos:
            raise ValueError("La categoría debe aplicar al menos a un tipo")
        self.nombre = nombre_limpio  # str (primitivo)
        self.emoji = emoji  # str (primitivo)
        self.tipos = frozenset(tipos_validos)  # conjunto de str

    def permite(self, tipo):
        """True si la categoría aparece en el formulario de ese tipo."""
        return tipo in self.tipos

    def __eq__(self, otra):
        if not isinstance(otra, Categoria):
            return NotImplemented
        return self.nombre == otra.nombre

    def __hash__(self):
        return hash(self.nombre)

    def __repr__(self):
        return f"Categoria({self.emoji} {self.nombre!r})"
