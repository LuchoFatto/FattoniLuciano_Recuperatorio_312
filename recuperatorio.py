from funciones_recu import *

primer_paso = False
segundo_paso = False

while True:
    match menu():
        case "1":
            nombre_archivo = input("Ingrese el nombre de archivo: ")
            lista_de_dicc = cargar_csv(nombre_archivo)
            primer_paso = True
        case "2":
            if primer_paso:
                mostrar_lista(cargar_csv(nombre_archivo))
            else:
                print("Debe cargar primero el archivo CSV")
        case "3":
            if primer_paso:
                peliculas_con_rating = mapear_lista(asignar_estadisticas_rating, lista_de_dicc)
                mostrar_lista(peliculas_con_rating)
                segundo_paso = True
            else:
                print("Debe cargar el archivo CSV")
        case "4":
            if segundo_paso:
                peliculas_con_genero = mapear_lista(asignar_estadisticas_genero, lista_de_dicc)
            else:
                print("Debe primero asignar estadísticas")
        case "5":
            if segundo_paso:
                genero_a_filtrar = input("Ingrese un género de pelicula (drama, comedia, acción, terror): ")
                genero_filtrado = filtrar_lista(lambda movie: filtro_por_genero(movie, genero_a_filtrar), lista_de_dicc)
                guardar_csv(f"{genero_a_filtrar}", genero_filtrado)
            else:
                print("Debe primero asignar estadísticas")
        case "6":
            if segundo_paso:
                peliculas_ordenadas = orden_lista(comparar_peliculas, lista_de_dicc)
                mostrar_lista(peliculas_ordenadas)
            else:
                print("Debe primero asignar estadísticas")
        case "7":
            if segundo_paso:
                print(mayor_rating(lista_de_dicc))
            else:
                print("Debe primero asignar estadísticas")
        case "8":
            if segundo_paso:
                mejor_pelicula = mayor_rating_lista(lista_de_dicc)
                guardar_datos_json("mejor_pelicula", mejor_pelicula)
            else:
                print("Debe primero asignar estadísticas")
        case "9":
            break














































