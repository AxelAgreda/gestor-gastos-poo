from datetime import date, datetime


class Movimiento:
    """Representa un gasto o un ingreso dentro del gestor de gastos."""

    # PÚBLICOS: constantes de la clase que el resto del programa necesita leer
    # (por ejemplo, para mostrar los tipos en la pantalla de registro).
    TIPOS = ("Gasto", "Ingreso")
    REGISTRAR_CICLO = True

    def __init__(self, id_mov, tipo, monto, categoria, descripcion, fecha):
        """Crea un movimiento nuevo.

        Parámetros:
            id_mov (int): número único del registro.
            tipo (str): "Gasto" o "Ingreso".
            monto (float): cantidad mayor que cero, con máximo dos decimales.
            categoria (str): por ejemplo "Supermercado" o "Transporte".
            descripcion (str): nota libre para recordar de qué fue el movimiento.
            fecha (date): día en que ocurrió.

        Lanza ValueError si el tipo no existe, si el monto no cumple la regla
        de es_monto_valido() o si la categoría viene vacía.
        """
        if tipo not in self.TIPOS:
            raise ValueError(f"Tipo no válido: {tipo}")

        # PRIVADO: el id identifica el registro y __eq__ y __hash__ dependen de él.
        # Si se pudiera cambiar desde afuera, un objeto guardado en un set quedaría
        # con un hash viejo y Python ya no lo encontraría.
        self.__id = id_mov

        # PRIVADO: pasar un gasto a ingreso cambia el balance en el doble del monto.
        # Si se registró mal, se borra y se registra de nuevo.
        self.__tipo = tipo

        # PROTEGIDO (_monto): en la Unidad 2 pienso crear las subclases Gasto e
        # Ingreso, que van a necesitar leerlo directamente. Desde afuera se usa la
        # property monto, que valida la regla antes de guardar el valor.
        self.monto = monto

        # PRIVADO: solo cambia con cambiar_categoria(), que limpia el texto. Así
        # "supermercado " y "Supermercado" no terminan como dos categorías distintas.
        self.__categoria = self._normalizar_categoria(categoria)

        # PÚBLICOS: no tienen ninguna regla que proteger. Ponerles property solo
        # agregaría código que no valida nada.
        self.descripcion = descripcion
        self.fecha = fecha

        if self.REGISTRAR_CICLO:
            print(f"  [CREACIÓN] Movimiento #{self.__id} creado "
                  f"({self.__tipo}, ${self._monto:,.2f})")

    def __del__(self):
        """Se ejecuta cuando el objeto se queda sin referencias. Solo evidencia
        esa etapa del ciclo de vida; no libera ningún recurso."""
        try:
            id_mov = self.__id
        except AttributeError:
            return      # el objeto falló en __init__ y nunca quedó completo
        if self.REGISTRAR_CICLO:
            print(f"  [DESTRUCCIÓN] Movimiento #{id_mov} liberado de la memoria")

    # ---------- Properties ----------
    @property
    def id(self):
        return self.__id            # sin setter: solo lectura

    @property
    def tipo(self):
        return self.__tipo          # sin setter: solo lectura

    @property
    def categoria(self):
        return self.__categoria     # se modifica con cambiar_categoria()

    @property
    def monto(self):
        return self._monto

    @monto.setter
    def monto(self, valor):
        if not self.es_monto_valido(valor):
            raise ValueError(f"Monto no válido: {valor}")
        self._monto = valor

    # ---------- Métodos públicos ----------
    def efecto_en_balance(self):
        """Un gasto resta al balance y un ingreso suma."""
        if self.__tipo == "Gasto":
            return -self._monto
        return self._monto

    def cambiar_categoria(self, nueva_categoria):
        """Corrige la categoría cuando el movimiento se registró mal."""
        self.__categoria = self._normalizar_categoria(nueva_categoria)

    def resumen(self):
        """Devuelve el movimiento en una línea, como se ve en el historial."""
        signo = "-" if self.__tipo == "Gasto" else "+"
        return f"{self.fecha:%d/%m/%Y}  {self.__categoria:<13} {signo}${self._monto:,.2f}"

    @classmethod
    def desde_texto(cls, linea):
        """Crea un movimiento a partir de una línea de texto con el formato
        id;tipo;monto;categoria;descripcion;dd/mm/aaaa
        """
        partes = [p.strip() for p in linea.split(";")]
        if len(partes) != 6:
            raise ValueError(f"La línea debe tener 6 campos y tiene {len(partes)}")
        id_txt, tipo, monto_txt, categoria, descripcion, fecha_txt = partes
        monto = float(monto_txt.replace("$", "").replace(",", ""))
        fecha = datetime.strptime(fecha_txt, "%d/%m/%Y").date()
        return cls(int(id_txt), tipo.capitalize(), monto, categoria, descripcion, fecha)

    @staticmethod
    def es_monto_valido(monto):
        """Regla del gestor: el monto es un número mayor que cero
        con máximo dos decimales."""
        if isinstance(monto, bool) or not isinstance(monto, (int, float)):
            return False
        return monto > 0 and round(monto, 2) == monto

    # ---------- Método protegido ----------
    @staticmethod
    def _normalizar_categoria(texto):
        """PROTEGIDO: ayuda interna que las subclases podrán reutilizar, pero que no
        forma parte de lo que el resto del programa necesita llamar."""
        limpio = " ".join(str(texto).split())
        if not limpio:
            raise ValueError("La categoría no puede estar vacía")
        return limpio.title()

    # ---------- Igualdad ----------
    def __eq__(self, otro):
        if not isinstance(otro, Movimiento):
            return NotImplemented
        return self.__id == otro.__id

    def __hash__(self):
        return hash(self.__id)
