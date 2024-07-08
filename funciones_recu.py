import random
import csv
import os
import json

def menu():
    print('''\n Ingrese una opcion: 
1) Cargar archivo CSV.

2) Se imprimirá por pantalla la tabla con los datos de las peliculas.

3) Asignar valor de rating de manera aleatoria.

4) Asignar género de pelicula de manera aleatoria.

5) Filtrar por género las peliculas.

6) Ordenar peliculas por genero y las del mismo genero en rating descendente.

7) Mostrar el titulo y el rating de la película con más rating.

8) Se guardará el listado del punto anterior en un archivo JSON.

9) Salir.\n''')
    return input("\n Ingrese una opcion: ")

def obtener_path_actual(nombre_archivo:str):
    """
        Se encarga de ubicar el archivo segun el nombre_archivo
    """
    directorio_actual = os.path.dirname(__file__)
    return os.path.join(directorio_actual, nombre_archivo)

def cargar_csv(nombre_archivo:str)->list:
    """
        Se encarga de cargar un archivo csv
        Retorna una lista de diccionarios
    """

    ruta_de_acceso = obtener_path_actual(f"{nombre_archivo}.csv")

    try:
        with open(ruta_de_acceso, "r", encoding= "utf-8") as archivo:
            lista_dicccionarios = []
            lector_csv = csv.DictReader(archivo)
            for fila in lector_csv:
                lista_dicccionarios.append(fila)

        print("Cargado con exito")
        return lista_dicccionarios
    except FileNotFoundError:
        print(f"Archivo {nombre_archivo} no encontrado.")

def guardar_csv(nombre_archivo_salida:str, lista:list):
    """
        Guardo el archivo csv
        En caso de existir te borra y sobreescribe lo anterior
    """
    ruta_salida = obtener_path_actual(f"{nombre_archivo_salida}.csv")

    with open(ruta_salida, "w", encoding="utf-8", newline='') as archivo_modificado:
        escritor_csv = csv.writer(archivo_modificado)
        for elementos in lista:
            escritor_csv.writerow([elementos["id"], elementos["titulo"], elementos["genero"], elementos["rating"]])

    print(f"El archivo {ruta_salida} se guardo correctamente!")

def guardar_datos_json(nombre_archivo_salida:str, lista:list):
    """
        Guardo el archivo en json
    """
    nueva_ruta = obtener_path_actual(f"{nombre_archivo_salida}.json")
    with open(nueva_ruta, "w", encoding = "utf-8") as archivo:
        json.dump(lista,archivo,indent=4)

    print(f"El archivo {nueva_ruta} se guardo correctamente!")

def mostrar_lista(lista:list):
    """
        Recibe una lista
        Imprime en terminal la lista
        En caso contrario devuelve un error por consola
    """
    if len(lista) > 0:
        print("id    titulo                              genero              rating")
        for elemento in lista:
            mostrar_consola(elemento)
    else:
        print("ERROR: No se puede recorrer la lista")

def mostrar_consola(elemento:dict):
    """
        Recibe un diccionario 
        Imprime en terminal cada elemento
    """
    print(f"{elemento["id"]:<5} {elemento["titulo"]:<30} {elemento["genero"]:>15} {elemento["rating"]:>10}")

def asignar_estadisticas_rating(pelicula:dict)->dict:
    """
        Recibe un diccionario
        Se encarga de manera aleatoria asignarle valores
    """
    pelicula["rating"] = random.randint(10, 100) / 10
    return pelicula

def asignar_estadisticas_genero(pelicula:dict)->dict:
    """
        Recibe un diccionario
        Se encarga de manera aleatoria asignarle valores
    """
    generos = {1: "drama", 2: "comedia", 3: "accion", 4: "terror"}
    pelicula["genero"] = generos[random.randint(1, 4)]
    return pelicula

def mapear_lista(funct,lista:list)->list:
    '''
        Recibe una lista,funcion
        Mapea la lista segun la criterio que se envie en funct
        Retorna la lista mapeada
        Caso contrario devuelve una lista vacia
    '''
    lista_nueva = []

    if(len(lista) > 0):
        for elem in lista:
            lista_nueva.append(funct(elem))

    return lista_nueva

def filtrar_lista(func, lista:list)->list:
    """
        Recibe una lista, funcion
        Filtra la lista segun la criterio que se envie en func
        En caso contrario devuelve una lista vacía
    """
    lista_nueva = []
    if len(lista) > 0:
        for elem in lista:
            if func(elem):
                lista_nueva.append(elem)
    return lista_nueva

def filtro_por_genero(pelicula: dict, genero_a_filtrar: str)->bool:
    """
        Función de filtro para películas por género
    """
    return pelicula["genero"].lower() == genero_a_filtrar.lower()

def orden_lista(func, lista:list)->None:
    """
        Recibe una lista
        Modifica segun el criterio de la funct
    """
    tam = len(lista)
    for i in range(tam - 1):
        for j in range(i + 1, tam):
            if func(lista[i], lista[j]):
                swaps_valores(lista,i,j)
    return lista

def swaps_valores(lista:list, i:int, j:int)->None:
    '''
        Recibe una lista 
        Se encarga de swappear tanto lo que viene en i y j
    '''
    aux = lista[i]
    lista[i] = lista[j]
    lista[j] = aux 

def comparar_peliculas(movie1: dict, movie2: dict)->bool:
    """
    Función de comparación para ordenar películas
    Se encarga de devolver las peliculas ordenadas por genero y aquellas que son de igual
    genero las poner en rating decreciente
    """
    if movie1["genero"] == movie2["genero"]:
        return float(movie1["rating"]) > float(movie2["rating"])
    else:
        return movie1["genero"] < movie2["genero"]

def mayor_menor(fun, lista:list)->dict:
    '''
        Recibe una lista de la cual filtra dependiendo del lambda
        Retorna un elemento
    '''  
    bandera = True
    for i in lista:
        if bandera or fun(i, item):
            bandera = False
            item = i
    return item

def mayor_rating(movies:dict)->str:
    """
        Me filtra la pelicula con mejor rating
    """
    mejor_pelicula = mayor_menor(lambda movie1, movie2: float(movie1["rating"]) > float(movie2["rating"]), movies)
    return f"titulo mejor rankeado: {mejor_pelicula["titulo"]} con rating de: {mejor_pelicula["rating"]}"

def mayor_rating_lista(movies: list)->list:
    """
        Encuentra la película con el mejor rating en la lista de películas.
        Retorna una lista con un diccionario que contiene el título y el rating de la película con el mejor rating.
    """
    mejor_pelicula = mayor_menor(lambda movie1, movie2: float(movie1["rating"]) > float(movie2["rating"]), movies)
    return [{"titulo": mejor_pelicula['titulo'], "rating": mejor_pelicula['rating']}]


















































































