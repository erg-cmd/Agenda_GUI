###############################################################
# @ Brief: TP_INICIAL
# @ Authors:
#           : Elias R Gracia Sosa
#           : Matias Damian Soto
# @ Date: 27/06/2021
# @ Update: 19/07/2021
# @ Comments: Version Final de Socios
###############################################################

# IMPORTS ---------------------------------

from time import sleep
from tkinter import messagebox
from turtle import bgcolor, title, window_width
import mysql.connector
import re
# DECLARACIONES ---------------------------

from tkinter import *
from tkinter.messagebox import showinfo, showerror
app = Tk()
app.title("Libro de Socios")  # el titulo de la ventana

# ---------------------------------------------------------
# STRING PARA MYSQL
string_tabla_vacia = "SELECT * from Tabla_Socios limit 1"
string_db = "CREATE DATABASE IF NOT EXISTS Club_Python"
string_usar_db = "USE Club_Python"
string_tabla = '''CREATE TABLE IF NOT EXISTS Tabla_Socios( 
    socio int(1) NOT NULL PRIMARY KEY AUTO_INCREMENT,
    nombre CHAR(20),
    apellido char(20),
    dni INT,
    domicilio CHAR(35), 
    localidad char(30), 
    nacionalidad CHAR(35),
    fnacimiento DATE, 
    meses_impagos CHAR(40))'''
string_socio = '''INSERT INTO Tabla_Socios (
    socio, nombre, apellido,dni,domicilio,localidad,
    nacionalidad, fnacimiento, meses_impagos) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'''
string_alta_socio = '''INSERT INTO Tabla_Socios (
    nombre, apellido,dni,domicilio,localidad,
    nacionalidad, fnacimiento, meses_impagos) 
    VALUES ( %s, %s, %s, %s, %s, %s, %s, %s)'''
string_modif_socio = '''UPDATE Tabla_Socios SET nombre=%s, apellido=%s,
    dni=%s,domicilio=%s,localidad=%s,nacionalidad=%s, fnacimiento=%s, meses_impagos=%s
    WHERE socio=%s'''
string_baja_socio = "DELETE FROM Tabla_Socios WHERE socio=%s"
string_busqueda_sql = ["socio", "nombre", "apellido", "dni", "domicilio",
                       "localidad", "nacionalidad", "fnacimiento", "meses_impagos"]
string_sql_socio1 = ["123456", "Elias", "Gracia",
                     "10456789", "Pasteur 260", "Lomas de Zamora", "Argentino",
                     "1999-01-20", "Debe todo el 2019"]
string_sql_socio2 = ["123457", "Juan", "Garcia",
                     "20459876", "Plank 170", "Cleypole", "Paraguayo",
                     "1990-02-24", "Abril2018"]
string_sql_socio3 = ["123458", "Alejandra", "Perez",
                     "39056789", "Einsten 100", "Lanus", "Uruguaya",
                     "1980-03-14", "Junio2019"]
string_sql_socio4 = ["123459", "Cecilia", "Ortega",
                     "92056789", "Milsten 998", "Avellaneda", "Brasilera",
                     "2010-04-04", "No adeuda"]

# para frame datos_socio
items_labels = ["Numero de Socio", "Nombre", "Apellido",
                "DNI", "Domicilio", "Localidad", "Nacionalidad",
                "Fecha de Nacimiento", "Meses Impagos"]
placeholders_labels_socio = ["123456", "Elias", "Gracia",
                             "12345678", "Calle 123", "Lomas de Zamora", "Argentino",
                             "2000-01-24", "Abril2018,Junio2019"]
placeholder_consulta_entry = "Ingrese aqui su busqueda"
placeholder_consulta_label = ["\n\nNo se han realizado consultas\n\n", "Se han encontrado",
                              "coincidencias", "\n\nNo se han encontrado coincidencias\n\n",
                              "\n\nNo se ha seleccionado categoria\n\n",
                              "\n\nCambios realizados exitosamente!\n\n"]
# strings REGEX
string_patron = ["^\d{1,5}$", "^[a-zA-Z]+$", "^[a-zA-Z]+$",
                 "([1-9][0-9]{6}$|[1-5][0-9]{7}$)",
                 "(^[a-zA-Z]+\s([a-zA-Z]+\s)?([a-zA-Z]+\s)?([a-zA-Z]+\s)?)\d{1,6}\Z",
                 '''(^(\d{1,2}) [a-zA-Z]+ ([a-zA-Z]+)?|(^[a-zA-Z]+$)|(^[a-zA-Z]+\s
                 ([a-zA-Z]+\s)?([a-zA-Z]+)\Z)|^[a-zA-Z]+ (\d{1,6})?\Z)''',
                 "^[a-zA-Z]{2,15}$", "(1|2)[0-9]{3}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])"
                 ]

# Variables Globales
cant_entries = 9
items_entries = []
items_botones = []
var_socio = []
var_borrado_entry = [1, 1, 1, 1, 1, 1, 1, 1, 1]

# FUNCIONES ------------------------------

# Funciones dummy para borrado de los placeholders


def func_clear_entry0(position):
    if var_borrado_entry[0]:
        items_entries[0].delete(0, "end")
        items_entries[0].config(fg="black")
        var_borrado_entry[0] = 0


def func_clear_entry1(position):
    if var_borrado_entry[1]:
        items_entries[1].delete(0, "end")
        items_entries[1].config(fg="black")
        var_borrado_entry[1] = 0


def func_clear_entry2(position):
    if var_borrado_entry[2]:
        items_entries[2].delete(0, "end")
        items_entries[2].config(fg="black")
        var_borrado_entry[2] = 0


def func_clear_entry3(position):
    if var_borrado_entry[3]:
        items_entries[3].delete(0, "end")
        items_entries[3].config(fg="black")
        var_borrado_entry[3] = 0


def func_clear_entry4(position):
    if var_borrado_entry[4]:
        items_entries[4].delete(0, "end")
        items_entries[4].config(fg="black")
        var_borrado_entry[4] = 0


def func_clear_entry5(position):
    if var_borrado_entry[5]:
        items_entries[5].delete(0, "end")
        items_entries[5].config(fg="black")
        var_borrado_entry[5] = 0


def func_clear_entry6(position):
    if var_borrado_entry[6]:
        items_entries[6].delete(0, "end")
        items_entries[6].config(fg="black")
        var_borrado_entry[6] = 0


def func_clear_entry7(position):
    if var_borrado_entry[7]:
        items_entries[7].delete(0, "end")
        items_entries[7].config(fg="black")
        var_borrado_entry[7] = 0


def func_clear_entry8(position):
    if var_borrado_entry[8]:
        items_entries[8].delete(0, "end")
        items_entries[8].config(fg="black")
        var_borrado_entry[8] = 0

# ---Func - func_init() --------


def func_init():
    # seteos botones
    for x in range(0, len(items_botones)):
        items_botones[x].grid(row=10, column=2*x, sticky="w", columnspan=1)
        items_botones[x].config(state=DISABLED)
    items_botones[0].config(state=NORMAL)
    items_botones[1].grid(row=0, column=3, rowspan=4,
                          columnspan=1, sticky='ns')
    func_borrarEntrys()
    # prefijar ayudas en entrys _ placeholder
    for x in range(1, cant_entries):  # que no escriba el numero de socio
        items_entries[x].insert(0, placeholders_labels_socio[x])
        items_entries[x].config(fg="grey")
    # seleccionamos por defecto la opcion Numero de Socio
    consulta_lista.selection_set(first=0)
    resultados_spinbox.config(state=NORMAL, from_=1,
                              to=10)  # Iniciamos el SpinBox
    resultados_spinbox.config(state=DISABLED)


def func_database_conectada():
    print("La base de datos esta conectada? " + str(miDB.is_connected()))
    if miDB.is_connected == FALSE:
        miDB.reconnect
        print("Se reconecto a la tabla")

# ---Func - func_alta() --------


def func_alta():
    try:
        func_database_conectada()
        if func_regex_extries():
            micursor = miDB.cursor()
            micursor.execute(string_alta_socio, var_socio)
            miDB.commit()
            print(micursor.rowcount, "Cantidad de registros agregados.")
            items_botones[1].config(state=NORMAL)
            resultados_spinbox.config(state=DISABLED)
        else:
            messagebox.showinfo(title="Datos de Socio",
                                message="Datos Inconsistentes")

    except:
        messagebox.showerror(title="Datos de Socio",
                             message="Datos Inconsistentes")

# ---Func --- func_consulta() ---------------


def func_consulta():
    global var_sql_resultado
    var_categoria = consulta_lista.curselection()
    if len(var_categoria) == 0:
        var_texto_consulta.set(placeholder_consulta_label[4])
        func_borrarEntrys()
        items_botones[2].config(state=DISABLED)  # boton modificar
        items_botones[3].config(state=DISABLED)  # boton borrar
        resultados_spinbox.config(state=DISABLED)
    else:
        var_sql_columna = string_busqueda_sql[var_categoria[0]]
        print("La categoria a buscar es: " +
              str(var_categoria[0]) + " y tu busqueda es: " + consulta_entry.get())
        var_consulta = consulta_entry.get()
        func_database_conectada()  # nos aseguramos que esta conectada
        micursor = miDB.cursor()
        sql = "SELECT * FROM Tabla_Socios WHERE " + \
            var_sql_columna+" LIKE '%"+var_consulta+"%'"
        try:
            micursor.execute(sql)
            var_sql_resultado = micursor.fetchall()

            # si hay una o mas coincidencias
            if len(var_sql_resultado) >= 1:
                var_texto_consulta.set(
                    "\n\nHay "+str(len(var_sql_resultado))+" coincidencias!\n\n")
                consulta_texto.grid(row=7, column=3, columnspan=2, sticky="S")
                for x in var_sql_resultado:
                    print(x)
                func_activar_resultados()
            else:
                var_texto_consulta.set(
                    placeholder_consulta_label[3]
                )
                consulta_texto.grid(row=7, column=3, columnspan=2, sticky="S")
        except:
            messagebox.showerror(title="Consulta de Datos",
                                 message="Error en la Consulta")

# ---Func --- func_modificar() ---------------


def func_modificar():
    print("Modificar datos")
    func_database_conectada()
    items_entries[0].config(state=NORMAL)
    try:
        if (func_regex_extries()):
            var_socio.append(items_entries[0].get())
            micursor = miDB.cursor()
            micursor.execute(string_modif_socio, var_socio)
            miDB.commit()
            print(micursor.rowcount, "Cantidad de registros afectados.")
            var_texto_consulta.set(
                placeholder_consulta_label[5])  # Info de exito
            consulta_texto.grid(row=7, column=3, columnspan=2, sticky="S")
            resultados_spinbox.config(state=DISABLED)
            func_borrarEntrys()
            var_sql_resultado = 0
            items_botones[2].config(state=DISABLED)  # boton modificar
            items_botones[3].config(state=DISABLED)  # boton borrar
        else:
            messagebox.showinfo(title="Modificacion de Datos",
                                message="No es posible modificar los datos")
    except:
        messagebox.showerror(title="Modificacion de Datos",
                             message="Error en base de datos o de Datos Ingresados")

# ---Func --- func_baja() ---------------


def func_baja():
    print("Dar de Baja")
    func_database_conectada()
    micursor = miDB.cursor()
    items_entries[0].config(state=NORMAL)
    var_dato = (items_entries[0].get(),)
    micursor.execute(string_baja_socio, var_dato)
    miDB.commit()
    print(micursor.rowcount, "Registro borrado")
    func_borrarEntrys()
    items_botones[2].config(state=DISABLED)  # boton modificar
    items_botones[3].config(state=DISABLED)  # boton borrar
    resultados_spinbox.config(state=DISABLED)
    items_entries[0].config(state=DISABLED)  # Deshabilitamos el n de socio
    messagebox.showinfo(title="Baja de Socio",
                        message="El socio ha sido borrado")
# ---Func --- borrarEntrys() ---------------


def func_borrarEntrys():
    for x in range(0, cant_entries):
        items_entries[x].delete(0, "end")

# ---Func --- func_tabla_vacia() ---------------


def func_tabla_vacia():
    global miDB
    micursor = miDB.cursor()

    # preguntamos si la tabla esta vacia
    micursor.execute(string_tabla_vacia)
    resultado = micursor.fetchall()
    if not resultado:
        print("La tabla esta vacia")
    else:
        print("La tabla no esta vacia")
        items_botones[1].config(state=NORMAL)

# ---Func --- func_activar_resultados() ---------------


def func_activar_resultados():
    resultados_spinbox.config(state=NORMAL, from_=1, to=len(var_sql_resultado))
    resultados_spinbox.grid(row=8, column=4, sticky='ws')

    # activamos el boton modificar y ponemos condicion en alta
    items_botones[2].config(state=NORMAL)  # boton modificar
    items_botones[3].config(state=NORMAL)  # boton borrar

    # condicion de alta para que no pise lo ya escrito

    # realizamos una primer carga
    items_entries[0].config(state=NORMAL)  # habilitamos el n de socio
    func_borrarEntrys()
    for x in range(0, cant_entries):
        items_entries[x].insert(0, var_sql_resultado[0][x])
        items_entries[x].config(fg="black")
    items_entries[0].config(state=DISABLED)

# ---Func --- func_tabla_vacia() ---------------


def func_mostrar_resultados():
    items_entries[0].config(state=NORMAL)
    func_borrarEntrys()
    var_spinbox_valor = int(resultados_spinbox.get())-1
    print("el valor del indice spinbox es:"+str(var_spinbox_valor))
    for x in range(0, cant_entries):
        items_entries[x].insert(0, var_sql_resultado[var_spinbox_valor][x])
        items_entries[x].config()
    items_entries[0].config(state=DISABLED)


def func_socios_de_prueba(condicion):
    if condicion == TRUE:
        func_database_conectada()
        micursor = miDB.cursor()
        micursor.execute(string_alta_socio, string_sql_socio1)
        micursor.execute(string_alta_socio, string_sql_socio2)
        micursor.execute(string_alta_socio, string_sql_socio3)
        micursor.execute(string_alta_socio, string_sql_socio4)
        miDB.commit()
        print(micursor.rowcount, "Cantidad de registros agregados.")


def func_regex_extries():
    try:
        var_socio.clear()
        for x in range(1, cant_entries-1):
            var_socio.append(items_entries[x].get())
            print(re.search(string_patron[x], var_socio[x-1]))
            if re.search(string_patron[x], var_socio[x-1]) == None:
                messagebox.showinfo(title="Datos de Socio",
                                    message="No hay coincidencia en: "+str(var_socio[x-1]))
                return FALSE
        # este ultimo no requiere comprobacion
        var_socio.append(items_entries[8].get())
        return TRUE
    except:
        messagebox.showerror(title="Datos de Socio",
                             message="Ha habido un error en los entries")

# ------------------------------------------------------
# MAIN -------------------------------------------------


# Definimos el label frame de Datos del asociado, Acciones y Consulta
frame_DatosAsociado = LabelFrame(app, text="Datos del Asociado:", bg="#80ff80")
frame_DatosAsociado.grid(row=0, column=0, columnspan=4, sticky='E')
frame_Consulta = LabelFrame(app, text="Consulta:", bg="#80ffff")
frame_Consulta.grid(row=0, column=4, columnspan=2,
                    rowspan=cant_entries, sticky='NS')
frame_Acciones = LabelFrame(app, text="Acciones:")
frame_Acciones.grid(row=cant_entries, column=0, columnspan=8, sticky='S')
frame_Resultados = LabelFrame(frame_Consulta, text="Resultados:")
frame_Resultados.grid(row=8, column=3, columnspan=2, rowspan=3, sticky='NS')
# frame_Consulta.grid()
# Frame Datos Asociaddo ---------
# Labels
for x in range(0, cant_entries):
    Label(frame_DatosAsociado, text=items_labels[x], bg="#80ff80").grid(
        row=x, column=0, columnspan=2, sticky="w")

# Entrys
for x in range(0, cant_entries):
    items_entries.append(Entry(frame_DatosAsociado))
    items_entries[x].grid(row=x, column=2, columnspan=2)

# Frame Consulta ---------------:
scroll_consulta = Scrollbar(frame_Consulta)
consulta_lista = Listbox(
    frame_Consulta, yscrollcommand=scroll_consulta.set, height=3, selectbackground="#3385ff")
for x in range(0, cant_entries):
    consulta_lista.insert(x, items_labels[x])
consulta_lista.grid(row=3, column=4, sticky="w")
scroll_consulta.grid(row=3, column=4, sticky="e")
scroll_consulta.config(command=consulta_lista.yview)
consulta_entry = Entry(frame_Consulta)

# Texto de ayuda en el Entry
consulta_entry.insert(INSERT, placeholder_consulta_entry)
consulta_entry.grid(row=1, column=4, columnspan=2, sticky="EW")

# modificar el texto de Label a traves de var_consulta_texto
var_texto_consulta = StringVar()
var_texto_consulta.set(placeholder_consulta_label[0])
consulta_texto = Label(
    frame_Consulta, textvariable=var_texto_consulta, bg="#80ffff")
consulta_texto.grid(row=7, column=3, columnspan=2, sticky="S")

# Frame Resultados ------------:
consulta_texto2 = Label(frame_Resultados, text="Coincidencia N:", bg="#80ffff")
consulta_texto2.grid(row=8, columnspan=4, sticky='es')
resultados_spinbox = Spinbox(
    frame_Resultados, state=DISABLED, command=func_mostrar_resultados)
resultados_spinbox.grid(row=8, column=4, sticky='ws')

# Frame Acciones --------------:
# ---botones
items_botones.append(Button(frame_Acciones, text="Alta", command=func_alta))
items_botones.append(
    Button(frame_Consulta, text="Consulta", command=func_consulta))
items_botones.append(
    Button(frame_Acciones, text="Modificar", command=func_modificar))
items_botones.append(Button(frame_Acciones, text="Baja", command=func_baja))

# enlazamos los eventos con los entrys
items_entries[0].bind("<Button-1>", func_clear_entry0)
items_entries[1].bind("<Button-1>", func_clear_entry1)
items_entries[2].bind("<Button-1>", func_clear_entry2)
items_entries[3].bind("<Button-1>", func_clear_entry3)
items_entries[4].bind("<Button-1>", func_clear_entry4)
items_entries[5].bind("<Button-1>", func_clear_entry5)
items_entries[6].bind("<Button-1>", func_clear_entry6)
items_entries[7].bind("<Button-1>", func_clear_entry7)
items_entries[8].bind("<Button-1>", func_clear_entry8)

# funcion que inicialice el estado de entrys y que botones estan habilitados
func_init()

# Conexion a Base de Datos + Loop ppal
try:
    miDB = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd=""
    )
    micursor = miDB.cursor()
    # creamos la base de datos -> Club_Python
    micursor.execute(string_db)
    # usamos la base de datos
    micursor.execute(string_usar_db)
    # creamos la tabla -> Tabla_Socios
    micursor.execute(string_tabla)
    # preguntamos si la tabla esta vacia
    func_tabla_vacia()
    # creamos socios para rellenar la tabla
    func_socios_de_prueba(FALSE)
    app.mainloop()  # bucle principal
except:
    print("No se puede conectart con el servidor MYSQL")

finally:
    if (miDB.is_connected()):
        micursor.close()
        miDB.close()
        print("La conexion ha sido cerrada")
# EOF
