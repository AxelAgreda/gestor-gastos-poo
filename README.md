# Gestor de gastos personales (POO en Python)

Proyecto de la materia Programación Orientada a Objetos (Universidad CETEC México / AVANZA).
Versión en Python, con programación orientada a objetos, del modelo de mi app de gastos
compartidos (Google Apps Script + Google Sheets): gastos, ingresos, ahorros y retiros de
ahorro, registrados por varios usuarios en una billetera con su propio pote de ahorros.

## Cómo ejecutarlo

En Google Colab o con Python 3.12 o superior:

```
python ejercicio5.py
python ejercicio6.py
```

## Estructura

| Archivo | Contenido |
|---|---|
| `movimiento.py` | Clase abstracta `Movimiento` y subclases `Gasto`, `Ingreso`, `Ahorro` y `Retiro` |
| `categoria.py` | Clase `Categoria` con emoji y los tipos en los que aparece |
| `usuario.py` | Clase `Usuario` |
| `pote_ahorro.py` | Clase `PoteDeAhorro` con el ahorro acumulado |
| `billetera.py` | Clase `Billetera` (agrupación de movimientos y composición con `PoteDeAhorro`) |
| `excepciones.py` | Errores propios del proyecto |
| `act1_movimiento.py`, `ej1_` a `ej3_movimiento.py` | Versiones anteriores, para ver la evolución |
| `ejercicio1.py` a `ejercicio6.py` | Scripts de prueba de cada ejercicio |

## Avance

- Actividad 1: clase `Movimiento` con encapsulamiento, métodos de clase y estáticos.
- Actividad 2: montos con `Decimal`, herencia, polimorfismo, clase abstracta,
  composición, agrupación y sobrecarga simulada.

Autor: Edwin Axel Agreda Hernández
