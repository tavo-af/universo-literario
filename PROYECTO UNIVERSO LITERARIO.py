import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import requests
import json
from cryptography.fernet import Fernet

# =========================
# CLAVE FERNET
# =========================
KEY = b"3NE9fwgeaoMoivvpMN4q3tW897s1L3IogflH9gTdgd8="
fernet = Fernet(KEY)

def descifrar(valor):
    return fernet.decrypt(valor.encode()).decode()


# =========================
# DATOS CIFRADOS
# =========================
MYSQL_HOST = "gAAAAABqUXZ0OyhfFYaXEtUyJbJCNvFKn2Vkzklj5izkrBjqcTb5q8Fme843hUn1rOQ6FW-zKQ5r-E23jmQit3FxgvS4-ojnQw=="
MYSQL_USER = "gAAAAABqUXZ0MZfEyrIzP1Mf9h1454IjAiWbDPjngn9dqxKOKmG1rpm-1Hqw5IMxgWPA7Bviwmnsn6NRrML66eCtXd1OTwAAbA=="
MYSQL_PASSWORD = "gAAAAABqUXZ01kew-rYJCq6z8gucCqKC3qOazSFc2b-E-vUpy-0f8SUxLlNUaz4nCnlKbQB-OYmFe_uPOzTsPVWyZtPJ-8DieQ=="
MYSQL_DATABASE = "gAAAAABqUXZ0VZXGS-lcJvlRvSoa-CenYZ-riv1lgg2U4NBY8_t5CkVs4ST4S284nCxkNsEdAkZlPvD6iozYPNiqSPYciNbg2LcOHc47it4hQCvai3LtpiQ="

SOLACE_USER = "gAAAAABqUXZ0R4oo1iEFnrTHgKi4ElEWU9nk_JUov3o61eSn6CK4-p0uVa2Sr4_-RhbTyrMHZEhICzW5I4k9G6tWNCwSZHxohEc1dAjvot7vnqWYnSa5pc0="
SOLACE_PASSWORD = "gAAAAABqUXZ0nnoLokBAK-N35tKblZFlrhBq7_2lIWFjrkurnHo4hoE6HUHhG9XqiDHYRnyH3-encv-CzgKnUHWiq0Tq5g39rZiC1oD6g2OVh2mO6qUJ8fM="
SOLACE_URL = "gAAAAABqUXZ06SHELIkZb-VY3gT3UO7mePt0Rad01o0mDHtRqyLo0wKSENcuZBNQInZEq7dsWFK5o6zectRAqf5vjc6vSy7BZSvuY8a-ZRM_AaoVLQz4brhBmW-qIPPa62sF2NBuv5tO0McAv-TM6beyr-D5KAt456JMmUkoIfcElpoqZxssIpamQTJKbXyRg1CMCCrQbr0V"

# =========================
# CONEXION MYSQL
# =========================
conexion = mysql.connector.connect(
    host=descifrar(MYSQL_HOST),
    user=descifrar(MYSQL_USER),
    password=descifrar(MYSQL_PASSWORD),
    database=descifrar(MYSQL_DATABASE)
)

cursor = conexion.cursor()

# =========================
# SOLACE REST
# =========================

def enviar_evento_prestamo(usuario, empleado, fecha):

    url = descifrar(SOLACE_URL)

    evento = {
        "evento": "Prestamo.Creado",
        "usuario": usuario,
        "empleado": empleado,
        "fecha": fecha
    }

    response = requests.post(
        url,
        data=json.dumps(evento),
        headers={
            "Content-Type": "application/json",
            "Solace-delivery-mode": "direct"
        },
        auth=(
            descifrar(SOLACE_USER),
            descifrar(SOLACE_PASSWORD)
        )
    )

    print(response.status_code)

# =========================
# ESTILOS
# =========================
COLOR_FONDO = "#2b1e2f"
COLOR_SECUNDARIO = "#e883cb"
COLOR_BOTON = "#d2cf34"
COLOR_TEXTO = "#ffffff"

# =========================
# FUNCIONES GENERALES
# =========================
def mostrar_tabla(tabla):
    try:

        if tabla == "Libros":
            consulta = """
            SELECT
                L.id_libro,
                L.titulo,
                A.nombre AS Autor,
                E.nombre AS Editorial,
                C.nombre AS Categoria,
                L.existencias
            FROM Libros L
            INNER JOIN Autores A ON L.id_autor = A.id_autor
            INNER JOIN Editoriales E ON L.id_editorial = E.id_editorial
            INNER JOIN Categorias C ON L.id_categoria = C.id_categoria
            """
            cursor.execute(consulta)
        else:
            cursor.execute(f"SELECT * FROM {tabla}")

        datos = cursor.fetchall()
        columnas = [d[0] for d in cursor.description]

        tree.delete(*tree.get_children())
        tree["columns"] = columnas
        tree["show"] = "headings"

        for col in columnas:
            tree.heading(col, text=col)
            tree.column(col, width=150)

        for fila in datos:
            tree.insert("", tk.END, values=fila)

    except Exception as e:
        messagebox.showerror("Error", str(e))

# =========================
# CRUD LIBROS
# =========================
def ventana_libros():
    win = tk.Toplevel(root)
    win.title("Administrar Libros")
    win.geometry("550x380")
    win.configure(bg=COLOR_FONDO)

    tk.Label(win, text="Título", bg=COLOR_FONDO, fg="white").grid(row=0, column=0, padx=5, pady=5)
    titulo = tk.Entry(win, width=30)
    titulo.grid(row=0, column=1)

    cursor.execute("SELECT id_autor, nombre FROM Autores")
    autores = cursor.fetchall()
    dic_autores = {nombre: id_autor for id_autor, nombre in autores}

    tk.Label(win, text="Autor", bg=COLOR_FONDO, fg="white").grid(row=1, column=0, padx=5, pady=5)
    autor = ttk.Combobox(win, values=list(dic_autores.keys()), state="readonly")
    autor.grid(row=1, column=1)

    cursor.execute("SELECT id_editorial, nombre FROM Editoriales")
    editoriales = cursor.fetchall()
    dic_editoriales = {nombre: id_editorial for id_editorial, nombre in editoriales}

    tk.Label(win, text="Editorial", bg=COLOR_FONDO, fg="white").grid(row=2, column=0, padx=5, pady=5)
    editorial = ttk.Combobox(win, values=list(dic_editoriales.keys()), state="readonly")
    editorial.grid(row=2, column=1)

    cursor.execute("SELECT id_categoria, nombre FROM Categorias")
    categorias = cursor.fetchall()
    dic_categorias = {nombre: id_categoria for id_categoria, nombre in categorias}

    tk.Label(win, text="Categoría", bg=COLOR_FONDO, fg="white").grid(row=3, column=0, padx=5, pady=5)
    categoria = ttk.Combobox(win, values=list(dic_categorias.keys()), state="readonly")
    categoria.grid(row=3, column=1)

    tk.Label(win, text="Existencias", bg=COLOR_FONDO, fg="white").grid(row=4, column=0, padx=5, pady=5)
    existencias = tk.Entry(win, width=30)
    existencias.grid(row=4, column=1)

    def agregar():
        try:
            sql = """
            INSERT INTO Libros
            (titulo,id_autor,id_editorial,id_categoria,existencias)
            VALUES (%s,%s,%s,%s,%s)
            """

            valores = (
                titulo.get(),
                dic_autores[autor.get()],
                dic_editoriales[editorial.get()],
                dic_categorias[categoria.get()],
                int(existencias.get())
            )

            cursor.execute(sql, valores)
            conexion.commit()

            messagebox.showinfo("Éxito", "Libro agregado correctamente")
            mostrar_tabla("Libros")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(
        win,
        text="Agregar Libro",
        bg=COLOR_BOTON,
        fg="white",
        font=("Arial", 10, "bold"),
        command=agregar
    ).grid(row=5, column=0, pady=20)

def eliminar_libro():
    seleccionado = tree.selection()

    if not seleccionado:
        messagebox.showwarning("Error", "Selecciona un libro")
        return

    valores = tree.item(seleccionado[0])["values"]

    try:
        id_libro = valores[0]
        cursor.execute("DELETE FROM Libros WHERE id_libro=%s", (id_libro,))
        conexion.commit()

        mostrar_tabla("Libros")
        messagebox.showinfo("Éxito", "Libro eliminado")

    except Exception as e:
        messagebox.showerror("Error", str(e))

def ventana_prestamos():
    win = tk.Toplevel(root)
    win.title("Administrar Prestamos")
    win.geometry("500x300")
    win.configure(bg=COLOR_FONDO)

    cursor.execute("SELECT id_usuario,nombre FROM Usuarios")
    usuarios = cursor.fetchall()
    dic_usuarios = {n:i for i,n in usuarios}

    cursor.execute("SELECT id_empleado,nombre FROM Empleados")
    empleados = cursor.fetchall()
    dic_empleados = {n:i for i,n in empleados}

    tk.Label(win,text="Usuario",bg=COLOR_FONDO,fg="white").grid(row=0,column=0,pady=5)
    usuario = ttk.Combobox(win,values=list(dic_usuarios.keys()),state="readonly")
    usuario.grid(row=0,column=1)

    tk.Label(win,text="Empleado",bg=COLOR_FONDO,fg="white").grid(row=1,column=0,pady=5)
    empleado = ttk.Combobox(win,values=list(dic_empleados.keys()),state="readonly")
    empleado.grid(row=1,column=1)

    tk.Label(win,text="Fecha (AAAA-MM-DD)",bg=COLOR_FONDO,fg="white").grid(row=2,column=0,pady=5)
    fecha = tk.Entry(win)
    fecha.grid(row=2,column=1)

    def agregar():

        sql = """
        INSERT INTO Prestamos(id_usuario,id_empleado,fecha_prestamo)
        VALUES(%s,%s,%s)
        """

        cursor.execute(
            sql,
            (
                dic_usuarios[usuario.get()],
                dic_empleados[empleado.get()],
                fecha.get()
            )
        )

        conexion.commit()

        enviar_evento_prestamo(
            usuario.get(),
            empleado.get(),
            fecha.get()
        )

        messagebox.showinfo(
            "Éxito",
            "Préstamo agregado y evento enviado a Solace"
        )

    tk.Button(
        win,
        text="Agregar",
        command=agregar
    ).grid(row=3,column=0,pady=20)


def eliminar_prestamo():
    seleccionado = tree.selection()

    if not seleccionado:
        messagebox.showwarning("Error", "Selecciona un préstamo")
        return

    valores = tree.item(seleccionado[0])["values"]

    try:
        id_prestamo = valores[0]

        cursor.execute(
            "DELETE FROM Prestamos WHERE id_prestamo=%s",
            (id_prestamo,)
        )

        conexion.commit()

        mostrar_tabla("Prestamos")

        messagebox.showinfo(
            "Éxito",
            "Préstamo eliminado"
        )

    except Exception as e:
        messagebox.showerror("Error", str(e))


def ventana_multas():
    win = tk.Toplevel(root)
    win.title("Administrar Multas")
    win.geometry("500x300")
    win.configure(bg=COLOR_FONDO)

    cursor.execute("SELECT id_usuario,nombre FROM Usuarios")
    usuarios = cursor.fetchall()
    dic_usuarios = {n:i for i,n in usuarios}

    tk.Label(win,text="Usuario",bg=COLOR_FONDO,fg="white").grid(row=0,column=0,pady=5)
    usuario = ttk.Combobox(win,values=list(dic_usuarios.keys()),state="readonly")
    usuario.grid(row=0,column=1)

    tk.Label(win,text="Monto",bg=COLOR_FONDO,fg="white").grid(row=1,column=0,pady=5)
    monto = tk.Entry(win)
    monto.grid(row=1,column=1)

    tk.Label(win,text="Motivo",bg=COLOR_FONDO,fg="white").grid(row=2,column=0,pady=5)
    motivo = tk.Entry(win)
    motivo.grid(row=2,column=1)

    def agregar():
        sql = """
        INSERT INTO Multas(id_usuario,monto,motivo)
        VALUES(%s,%s,%s)
        """
        cursor.execute(sql,(
            dic_usuarios[usuario.get()],
            monto.get(),
            motivo.get()
        ))
        conexion.commit()
        messagebox.showinfo("Éxito","Multa agregada")

    tk.Button(win,text="Agregar",command=agregar).grid(row=3,column=0,pady=20)

def eliminar_multa():
    seleccionado = tree.selection()

    if not seleccionado:
        messagebox.showwarning("Error", "Selecciona una multa")
        return

    valores = tree.item(seleccionado[0])["values"]

    try:
        id_multa = valores[0]

        cursor.execute(
            "DELETE FROM Multas WHERE id_multa=%s",
            (id_multa,)
        )

        conexion.commit()

        mostrar_tabla("Multas")

        messagebox.showinfo(
            "Éxito",
            "Multa eliminada"
        )

    except Exception as e:
        messagebox.showerror("Error", str(e))


# =========================
# VENTANA PRINCIPAL
# =========================
root = tk.Tk()
root.title("Sistema UniversoLiterario")
root.geometry("1250x700")
root.configure(bg=COLOR_FONDO)

style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Treeview",
    background=COLOR_SECUNDARIO,
    foreground="white",
    fieldbackground=COLOR_SECUNDARIO,
    rowheight=28
)

style.configure(
    "Treeview.Heading",
    background=COLOR_BOTON,
    foreground="white",
    font=("Arial", 10, "bold")
)

titulo_app = tk.Label(
    root,
    text="📚 Sistema Universo Literario",
    bg=COLOR_FONDO,
    fg="white",
    font=("Arial", 18, "bold")
)
titulo_app.pack(pady=10)

barra = tk.Menu(root)
root.config(menu=barra)

menu_tablas = tk.Menu(barra, tearoff=0)
barra.add_cascade(label="Tablas", menu=menu_tablas)

tablas = [
    "Autores", "Editoriales", "Categorias",
    "Usuarios", "Empleados", "Libros",
    "Prestamos", "Devoluciones", "Multas"
]

for tabla in tablas:
    menu_tablas.add_command(
        label=tabla,
        command=lambda t=tabla: mostrar_tabla(t)
    )

menu_libros = tk.Menu(barra, tearoff=0)
barra.add_cascade(label="Libros", menu=menu_libros)

menu_libros.add_command(
    label="Administrar Libros",
    command=ventana_libros
)

menu_libros.add_command(
    label="Eliminar Libro Seleccionado",
    command=eliminar_libro
)
# =========================
# MENU PRESTAMOS
# =========================
menu_prestamos = tk.Menu(barra, tearoff=0)
barra.add_cascade(label="Prestamos", menu=menu_prestamos)

menu_prestamos.add_command(
    label="Administrar Prestamos",
    command=ventana_prestamos
)


menu_prestamos.add_command(
    label="Eliminar Prestamo Seleccionado",
    command=eliminar_prestamo
)
# =========================
# MENU MULTAS
# =========================
menu_multas = tk.Menu(barra, tearoff=0)
barra.add_cascade(label="Multas", menu=menu_multas)

menu_multas.add_command(
    label="Administrar Multas",
    command=ventana_multas
)

menu_multas.add_command(
    label="Eliminar Multa Seleccionada",
    command=eliminar_multa
)

frame = tk.Frame(root, bg=COLOR_FONDO)
frame.pack(fill="both", expand=True, padx=10, pady=10)

tree = ttk.Treeview(frame)
tree.pack(fill="both", expand=True)

mostrar_tabla("Libros")

root.mainloop()

cursor.close()
conexion.close()

