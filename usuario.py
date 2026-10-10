"""Usuarios que comparten la app, como en la hoja Usuarios."""


class Usuario:
    """Persona que registra movimientos."""

    def __init__(self, id_usuario, nombre):
        nombre_limpio = " ".join(str(nombre).split())
        if not nombre_limpio:
            raise ValueError("El usuario necesita un nombre")
        self.id = id_usuario  # int (primitivo)
        self.nombre = nombre_limpio  # str (primitivo)
        # En la app el borrado es suave: el usuario se desactiva, pero su
        # historial de movimientos se conserva.
        self.activo = True  # bool (primitivo)

    def desactivar(self):
        self.activo = False

    def __repr__(self):
        return f"Usuario({self.nombre!r})"
