
import sqlite3
import os

# ==========================================
# MÓDULO 1. CREACIÓN DE LA BASE DE DATOS
# ==========================================

def crear_bd():
    os.makedirs("database", exist_ok=True)

    conexion = sqlite3.connect("database/alumnos.db")
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alumno (
            matricula TEXT PRIMARY KEY,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            calle TEXT,
            colonia TEXT,
            padre_tutor TEXT,
            tel_tutor TEXT
        )
    """)

    conexion.commit()
    conexion.close()

    print("Base de datos creada correctamente.")


# ==========================================
# MÓDULO 2. ALTA DE ALUMNOS
# ==========================================

def alta_alumno():
    print("\n===== ALTA DE ALUMNO =====")

    matricula = input("Matrícula: ").strip()
    nombre = input("Nombre: ").strip()
    apellido = input("Apellido: ").strip()
    calle = input("Calle: ").strip()
    colonia = input("Colonia: ").strip()
    padre_tutor = input("Nombre del padre o tutor: ").strip()
    tel_tutor = input("Teléfono del tutor: ").strip()

    if not matricula or not nombre or not apellido:
        print("Error: matrícula, nombre y apellido son obligatorios.")
        return

    try:
        with sqlite3.connect("database/alumnos.db") as conexion:
            conexion.execute("""
                INSERT INTO alumno (
                    matricula, nombre, apellido, calle,
                    colonia, padre_tutor, tel_tutor
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                matricula, nombre, apellido, calle,
                colonia, padre_tutor, tel_tutor
            ))

        print("Alumno registrado correctamente.")

    except sqlite3.IntegrityError:
        print("Error: la matrícula ya existe.")

    except sqlite3.Error as error:
        print(f"Error al registrar al alumno: {error}")


# ==========================================
# MÓDULO 3. CONSULTAR ALUMNOS
# ==========================================

def consultar_alumnos():
    print("\n===== CONSULTA DE ALUMNOS =====")
    print("1. Consultar todos los alumnos")
    print("2. Buscar por matrícula")

    opcion = input("Selecciona una opción: ").strip()

    try:
        with sqlite3.connect("database/alumnos.db") as conexion:
            cursor = conexion.cursor()

            if opcion == "1":
                cursor.execute("""
                    SELECT * FROM alumno ORDER BY apellido, nombre
                """)
            elif opcion == "2":
                matricula = input("Matrícula a buscar: ").strip()
                cursor.execute("""
                    SELECT * FROM alumno WHERE matricula = ?
                """, (matricula,))
            else:
                print("Opción no válida.")
                return

            alumnos = cursor.fetchall()

            if not alumnos:
                print("No se encontraron alumnos.")
                return

            for alumno in alumnos:
                mostrar_alumno(alumno)

    except sqlite3.Error as error:
        print(f"Error al consultar alumnos: {error}")


def mostrar_alumno(alumno):
    print("\n------------------------------")
    print(f"Matrícula: {alumno[0]}")
    print(f"Nombre: {alumno[1]}")
    print(f"Apellido: {alumno[2]}")
    print(f"Calle: {alumno[3] or 'No registrado'}")
    print(f"Colonia: {alumno[4] or 'No registrada'}")
    print(f"Padre o tutor: {alumno[5] or 'No registrado'}")
    print(f"Teléfono del tutor: {alumno[6] or 'No registrado'}")
    print("------------------------------")


# ==========================================
# MÓDULO 4. MODIFICAR ALUMNOS
# ==========================================

def modificar_alumno():
    print("\n===== MODIFICAR ALUMNO =====")

    matricula = input("Matrícula del alumno a modificar: ").strip()

    try:
        with sqlite3.connect("database/alumnos.db") as conexion:
            cursor = conexion.cursor()

            cursor.execute("""
                SELECT * FROM alumno WHERE matricula = ?
            """, (matricula,))

            alumno = cursor.fetchone()

            if alumno is None:
                print("No existe un alumno con esa matrícula.")
                return

            mostrar_alumno(alumno)
            print("\nEscribe el nuevo dato o presiona ENTER")
            print("para conservar el dato actual.")

            nombre = input(f"Nombre [{alumno[1]}]: ").strip()
            apellido = input(f"Apellido [{alumno[2]}]: ").strip()
            calle = input(f"Calle [{alumno[3] or ''}]: ").strip()
            colonia = input(f"Colonia [{alumno[4] or ''}]: ").strip()
            padre_tutor = input(
                f"Padre o tutor [{alumno[5] or ''}]: "
            ).strip()
            tel_tutor = input(
                f"Teléfono [{alumno[6] or ''}]: "
            ).strip()

            # Conservar los valores anteriores si se deja vacío
            nombre = nombre or alumno[1]
            apellido = apellido or alumno[2]
            calle = calle or alumno[3]
            colonia = colonia or alumno[4]
            padre_tutor = padre_tutor or alumno[5]
            tel_tutor = tel_tutor or alumno[6]

            cursor.execute("""
                UPDATE alumno
                SET nombre = ?,
                    apellido = ?,
                    calle = ?,
                    colonia = ?,
                    padre_tutor = ?,
                    tel_tutor = ?
                WHERE matricula = ?
            """, (
                nombre, apellido, calle, colonia,
                padre_tutor, tel_tutor, matricula
            ))

        print("Alumno modificado correctamente.")

    except sqlite3.Error as error:
        print(f"Error al modificar al alumno: {error}")


# ==========================================
# MÓDULO 5. ELIMINAR ALUMNOS
# ==========================================

def eliminar_alumno():
    print("\n===== ELIMINAR ALUMNO =====")

    matricula = input("Matrícula del alumno a eliminar: ").strip()

    try:
        with sqlite3.connect("database/alumnos.db") as conexion:
            cursor = conexion.cursor()

            cursor.execute("""
                SELECT * FROM alumno WHERE matricula = ?
            """, (matricula,))

            alumno = cursor.fetchone()

            if alumno is None:
                print("No existe un alumno con esa matrícula.")
                return

            mostrar_alumno(alumno)

            confirmar = input(
                "¿Seguro que deseas eliminarlo? (S/N): "
            ).strip().upper()

            if confirmar != "S":
                print("Eliminación cancelada.")
                return

            cursor.execute("""
                DELETE FROM alumno WHERE matricula = ?
            """, (matricula,))

        print("Alumno eliminado correctamente.")

    except sqlite3.Error as error:
        print(f"Error al eliminar al alumno: {error}")


# ==========================================
# MÓDULO 6. MENÚ PRINCIPAL
# ==========================================

def menu_principal():
    while True:
        print("\n================================")
        print(" SISTEMA DE CONTROL DE ALUMNOS")
        print("================================")
        print("1. Registrar alumno")
        print("2. Consultar alumnos")
        print("3. Modificar alumno")
        print("4. Eliminar alumno")
        print("5. Salir")
        print("================================")

        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            alta_alumno()
        elif opcion == "2":
            consultar_alumnos()
        elif opcion == "3":
            modificar_alumno()
        elif opcion == "4":
            eliminar_alumno()
        elif opcion == "5":
            print("Saliendo del sistema. ¡Hasta pronto!")
            break
        else:
            print("Opción no válida. Intenta nuevamente.")


# ==========================================
# PROGRAMA PRINCIPAL
# ==========================================

if __name__ == "__main__":
    crear_bd()
    menu_principal()
