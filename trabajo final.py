import os
from datetime import datetime  # Módulo para registrar la fecha y hora de las ventas

# Nombres de los archivos planos para guardar la información
ARCHIVO_INVENTARIO = "inventario.txt"
ARCHIVO_VENTAS = "ventas.txt"

# ==========================================
# 1. PERSISTENCIA DE DATOS (ARCHIVOS TXT)
# ==========================================

def cargar_inventario():
    """Lee el archivo inventario.txt al iniciar para recuperar los productos."""
    productos = {}
    if not os.path.exists(ARCHIVO_INVENTARIO):
        return productos
    
    try:
        with open(ARCHIVO_INVENTARIO, "r", encoding="utf-8") as file:
            for linea in file:
                linea = linea.strip()
                if linea:
                    partes = linea.split(",")
                    if len(partes) == 4:
                        id_prod, nombre, precio, stock = partes
                        productos[int(id_prod)] = {
                            'nombre': nombre,
                            'precio': float(precio),
                            'stock': int(stock)
                        }
    except FileNotFoundError:
        print("[!] Archivo de inventario no encontrado. Se creará uno nuevo.")
    except ValueError:
        print("[!] Error al leer el formato de datos en inventario.txt.")
    return productos


def guardar_inventario(productos):
    """Sobrescribe el archivo de inventario con los datos actualizados."""
    try:
        with open(ARCHIVO_INVENTARIO, "w", encoding="utf-8") as file:
            for id_prod, datos in productos.items():
                file.write(f"{id_prod},{datos['nombre']},{datos['precio']},{datos['stock']}\n")
    except IOError:
        print("[!] Error de escritura al intentar guardar el inventario.")


def registrar_venta_archivo(id_prod, nombre, cantidad, total):
    """Anexa cada transacción de venta al final del archivo ventas.txt."""
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(ARCHIVO_VENTAS, "a", encoding="utf-8") as file:
            file.write(f"{fecha_actual},{id_prod},{nombre},{cantidad},{total:.2f}\n")
    except IOError:
        print("[!] No se pudo registrar la venta en el archivo.")

# ==========================================
# 2. FUNCIONES MODULARES DEL SISTEMA
# ==========================================

def obtener_siguiente_id(productos):
    """Genera automáticamente el siguiente ID numérico correlativo."""
    if not productos:
        return 1
    return max(productos.keys()) + 1


def registrar_producto(productos):
    """Registra un nuevo producto solicitando datos y validando entradas."""
    print('\n-- Registrar producto --')
    nombre_producto = input('Ingrese nombre del producto: ').strip()
    if not nombre_producto:
        print('[!] Error: El nombre del producto no puede estar vacío.')
        return

    try:
        precio = float(input('Ingresa el precio ($): '))
        stock = int(input('Ingresa el stock inicial: '))

        if precio <= 0 or stock < 0:
            print('[!] Error: El precio debe ser positivo y el stock no puede ser negativo.')
            return

        id_prod = obtener_siguiente_id(productos)
        productos[id_prod] = {
            'nombre': nombre_producto,
            'precio': precio,
            'stock': stock
        }

        guardar_inventario(productos)
        print('[✓] Producto registrado correctamente.')
        print('ID asignado:', id_prod)

    except ValueError:
        print('[!] Error: Ingrese valores numéricos válidos para precio y stock.')


def actualizar_stock(productos):
    """Actualiza la cantidad de stock de un producto existente."""
    print('\n-- Actualizar stock --')
    try:
        id_prod = int(input('Ingrese el ID del producto: '))
        if id_prod in productos:
            nuevo_stock = int(input('Ingrese la cantidad a añadir al stock: '))
            if nuevo_stock < 0:
                print('[!] Error: La cantidad a añadir no puede ser negativa.')
                return

            productos[id_prod]['stock'] += nuevo_stock
            guardar_inventario(productos)
            print('[✓] Stock actualizado correctamente.')
            print('Nuevo stock:', productos[id_prod]['stock'])
        else:
            print('[!] Error: El producto con ese ID no existe.')
    except ValueError:
        print('[!] Error: Debe ingresar un valor numérico entero.')


def realizar_venta(productos):
    """Procesa la venta de un producto y descuenta el stock disponible."""
    print('\n-- Realizar Venta --')
    if not productos:
        print('[!] No hay productos registrados en el inventario.')
        return

    try:
        id_prod = int(input('Ingrese el ID del producto a vender: '))
        if id_prod not in productos:
            print('[!] Error: El producto no existe.')
            return

        prod = productos[id_prod]
        cantidad = int(input(f"Cantidad a vender (Stock actual: {prod['stock']}): "))

        if cantidad <= 0:
            print('[!] La cantidad a vender debe ser mayor a 0.')
            return
        if cantidad > prod['stock']:
            print('[!] Venta cancelada: Stock insuficiente.')
            return

        total = cantidad * prod['precio']
        prod['stock'] -= cantidad

        guardar_inventario(productos)
        registrar_venta_archivo(id_prod, prod['nombre'], cantidad, total)

        print('\n' + '='*30)
        print('      TICKET DE VENTA')
        print('='*30)
        print(f"Producto : {prod['nombre']}")
        print(f"Cantidad : {cantidad}")
        print(f"Total    : ${total:.2f}")
        print('='*30)
        print('[✓] Venta procesada exitosamente.')

    except ValueError:
        print('[!] Error: Ingrese un número válido.')


def consultar_inventario(productos):
    """Muestra la lista completa de productos registrados."""
    print('\n-- Catálogo de Inventario --')
    if not productos:
        print('El inventario se encuentra vacío.')
        return

    print(f"{'ID':<6} | {'Nombre':<20} | {'Precio':<10} | {'Stock':<8}")
    print('-' * 50)
    for id_p, d in productos.items():
        print(f"{id_p:<6} | {d['nombre']:<20} | ${d['precio']:<9.2f} | {d['stock']:<8}")


def reporte_ventas():
    """Muestra el historial de ventas registradas en ventas.txt."""
    print('\n-- Reporte General de Ventas --')
    if not os.path.exists(ARCHIVO_VENTAS):
        print('Aún no existen ventas registradas.')
        return

    total_ingresos = 0.0
    total_unidades = 0

    try:
        with open(ARCHIVO_VENTAS, 'r', encoding='utf-8') as file:
            print(f"{'Fecha y Hora':<20} | {'ID':<5} | {'Producto':<15} | {'Cant':<5} | {'Total':<8}")
            print('-' * 60)
            for linea in file:
                partes = linea.strip().split(',')
                if len(partes) == 5:
                    fecha, id_p, nom, cant, tot = partes
                    total_unidades += int(cant)
                    total_ingresos += float(tot)
                    print(f"{fecha:<20} | {id_p:<5} | {nom:<15} | {cant:<5} | ${tot:<8}")

        print('-' * 60)
        print(f"Total Unidades Vendidas : {total_unidades}")
        print(f"Ingresos Totales        : ${total_ingresos:.2f}")
    except (FileNotFoundError, ValueError):
        print('[!] Ocurrió un inconveniente al leer el archivo de ventas.')

# ==========================================
# 3. INTERFAZ Y MENÚ PRINCIPAL
# ==========================================

def main():
    productos = cargar_inventario()

    while True:
        print('\n' + '='*40)
        print(' SISTEMA DE GESTIÓN Y VENTAS ')
        print('='*40)
        print('1. Registrar Producto')
        print('2. Actualizar Stock')
        print('3. Realizar Venta')
        print('4. Consultar Inventario')
        print('5. Reporte de Ventas')
        print('6. Salir')
        print('='*40)

        opcion = input('Selecciona una opción (1-6): ').strip()

        if opcion == '1':
            registrar_producto(productos)
        elif opcion == '2':
            actualizar_stock(productos)
        elif opcion == '3':
            realizar_venta(productos)
        elif opcion == '4':
            consultar_inventario(productos)
        elif opcion == '5':
            reporte_ventas()
        elif opcion == '6':
            print('\n¡Guardando datos y saliendo del sistema!')
            break
        else:
            print('[!] Opción no válida. Intente nuevamente.')
            input('Presione ENTER para continuar...')

if __name__ == '__main__':
    main()