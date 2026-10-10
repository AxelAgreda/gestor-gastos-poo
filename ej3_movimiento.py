from datetime import datetime
from decimal import Decimal, InvalidOperation

# Un centavo: sirve para validar y redondear montos a dos decimales
CENTAVO = Decimal("0.01")
# Campos que debe traer una línea exportada: id;tipo;monto;categoria;descripcion;fecha
CAMPOS_POR_LINEA = 6
FORMATO_FECHA = "%d/%m/%Y"


# PILAR 1: ABSTRACCIÓN
# La clase modela solo lo que el gestor necesita saber de un movimiento: monto,
# categoría, fecha y descripción. Deja fuera detalles reales que no aportan nada,
# como el banco, el número de tarjeta o la hora exacta. Además, quien la usa llama
# efecto_en_balance() o resumen() sin saber cómo se calculan por dentro.
class Movimiento:
    """Representa un gasto o un ingreso dentro del gestor de gastos."""

    # PÚBLICOS: constantes de la clase que el resto del programa necesita leer
    # (por ejemplo, para mostrar los tipos en la pantalla de registro).
    TIPOS = ("Gasto", "Ingreso")

    def __init__(self, id_mov, tipo, monto, categoria, descripcion, fecha):
        """Crea un movimiento nuevo.

        Parámetros:
            id_mov (int): número único del registro.
            tipo (str): "Gasto" o "Ingreso".
            monto (Decimal, int o str): mayor que cero, con máximo dos decimales.
                Se guarda como Decimal para que las sumas de dinero sean exactas.
            categoria (str): por ejemplo "Supermercado" o "Transporte".
            descripcion (str): nota libre para recordar de qué fue el movimiento.
            fecha (date): día en que ocurrió.

        Lanza ValueError si el tipo no existe, si el monto no cumple la regla
        de es_monto_valido() o si la categoría viene vacía.
        """
        if tipo not in self.TIPOS:
            raise ValueError(f"Tipo no válido: {tipo}")

        # PILAR 2: ENCAPSULAMIENTO
        # Los atributos con doble guion bajo solo se leen con properties y el monto
        # solo se cambia con un setter que valida. Nadie de afuera puede dejar el
        # objeto en un estado inválido, como un monto negativo.

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

    # ---------- Properties ----------
    @property
    def id(self):
        return self.__id  # sin setter: solo lectura

    @property
    def tipo(self):
        return self.__tipo  # sin setter: solo lectura

    @property
    def categoria(self):
        return self.__categoria  # se modifica con cambiar_categoria()

    @property
    def monto(self):
        return self._monto

    @monto.setter
    def monto(self, valor):
        if not self.es_monto_valido(valor):
            raise ValueError(f"Monto no válido: {valor}")
        # CAMBIO (Ejercicio 1): antes se guardaba el float tal cual. Ahora se
        # convierte a Decimal pasando por str(), así 0.1 se guarda como 0.10 exacto
        self._monto = Decimal(str(valor)).quantize(CENTAVO)

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
        fecha_texto = self.fecha.strftime(FORMATO_FECHA)
        return f"{fecha_texto}  {self.__categoria:<13} {signo}${self._monto:,.2f}"

    @classmethod
    def desde_texto(cls, linea):
        """Crea un movimiento a partir de una línea de texto con el formato
        id;tipo;monto;categoria;descripcion;dd/mm/aaaa
        """
        campos = cls._separar_campos(linea)
        id_texto, tipo, monto_texto, categoria, descripcion, fecha_texto = campos
        return cls(
            int(id_texto),
            tipo.capitalize(),
            cls._limpiar_monto(monto_texto),
            categoria,
            descripcion,
            datetime.strptime(fecha_texto, FORMATO_FECHA).date(),
        )

    @staticmethod
    def _separar_campos(linea):
        """Divide la línea por punto y coma y revisa que traiga todos los campos."""
        campos = [campo.strip() for campo in linea.split(";")]
        if len(campos) != CAMPOS_POR_LINEA:
            raise ValueError(
                f"La línea debe tener {CAMPOS_POR_LINEA} campos y tiene {len(campos)}"
            )
        return campos

    @staticmethod
    def _limpiar_monto(monto_texto):
        """Quita el signo de dólar y la coma de miles: "$1,250.75" -> "1250.75"."""
        return monto_texto.replace("$", "").replace(",", "")

    @staticmethod
    def es_monto_valido(monto):
        """Regla del gestor: el monto es mayor que cero y tiene máximo dos decimales.
        Acepta int, float, Decimal o texto como "12.50"."""
        if isinstance(monto, bool):
            return False
        try:
            valor = Decimal(str(monto))
            return valor.is_finite() and valor > 0 and valor == valor.quantize(CENTAVO)
        except InvalidOperation:
            return False

    # ---------- Método protegido ----------
    @staticmethod
    def _normalizar_categoria(categoria):
        """PROTEGIDO: ayuda interna que las subclases podrán reutilizar, pero que no
        forma parte de lo que el resto del programa necesita llamar."""
        sin_espacios_extra = " ".join(str(categoria).split())
        if not sin_espacios_extra:
            raise ValueError("La categoría no puede estar vacía")
        return sin_espacios_extra.title()

    # ---------- Igualdad ----------
    def __eq__(self, otro):
        if not isinstance(otro, Movimiento):
            return NotImplemented
        return self.__id == otro.__id

    def __hash__(self):
        return hash(self.__id)


# PILAR 3: HERENCIA
# Ingreso ES UN Movimiento: hereda el id, el monto, la categoría, la validación y
# los métodos del padre, y solo agrega lo que lo hace distinto. En mi app real,
# los campos Fecha de pago y Período solo aparecen cuando el tipo es Ingreso.
class Ingreso(Movimiento):
    """Dinero que entra, como el pago de la quincena."""

    def __init__(self, id_mov, monto, categoria, descripcion, fecha, periodo=""):
        # super() reutiliza toda la validación del padre; el tipo siempre es "Ingreso"
        super().__init__(id_mov, "Ingreso", monto, categoria, descripcion, fecha)
        self.periodo = " ".join(str(periodo).split())  # ej. "1-15 oct"

    # PILAR 4: POLIMORFISMO
    # Sobrescribe resumen(). Cuando el historial llama movimiento.resumen(), Python
    # decide en tiempo de ejecución qué versión usar según la clase del objeto.
    def resumen(self):
        if not self.periodo:
            return super().resumen()
        return f"{super().resumen()}  (periodo: {self.periodo})"
