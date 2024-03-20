from fastapi import FastAPI
import api_data  # Archivo del repositorio, donde se cargan los dataframes requeridos 


# Instanciamos FastAPI
app = FastAPI()


@app.get('/PlayTimeGenre/{genero}')
def PlayTimeGenre(genero: str):
    """Devuelve el año con más horas jugadas para dicho género.
    """
    genero = str(genero).lower()  # Conversion a todo-minúsculas
    # Guard-clause que verifica si 'genero' es una entrada válida
    if not genero in api_data.df_generos_year_playtime.columns[4:]:
        return f'"{genero}" no es un género válido.'

    # Filtramos filas 'df_generos_year_playtime' donde el valor = True
    df_genero = api_data.df_generos_year_playtime[api_data.df_generos_year_playtime[genero] == True]
    
    # Obtenemos el año con más horas jugadas agrupando por 'release_year' y sumando los 'playtime_forever'
    # La fila con la suma de 'playtime_forever' mayor tiene el año como indice
    anio_maxplaytime = df_genero.groupby('release_year')['playtime_forever'].sum().idxmax()
    respuesta_api = {f"Año de lanzamiento con más horas jugadas para género {genero.title()}": anio_maxplaytime.year}
    
    return respuesta_api


@app.get('/UserForGenre/{genero}')
def UserForGenre(genero: str):
    """Devuelve el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año.
    """
    genero = str(genero).lower()  # Conversion a todo-minúsculas
    # Guard-clause que verifica si 'genero' es una entrada válida
    if not genero in api_data.df_maxplay_por_genero['genero'].values:
        return f'"{genero}" no es un género válido.'

    # Extraemos 'user_id', filtrando las filas donde la columna 'genero' = 'genero'
    usuario_maxplay_por_genero = api_data.df_maxplay_por_genero.loc[api_data.df_maxplay_por_genero['genero'] == genero, 'user_id'].iloc[0]
    # Iniciamos la construcción de la respuesta del API con la consulta previa
    respuesta_api = {
        f'Usuario con más horas jugadas para género {genero.title()}': usuario_maxplay_por_genero,
    }

    # Filtramos para el género y el usuario correspondiente, para años con 'playtime_forever' > 0
    df_filtrado = api_data.df_play_por_genero_anio[
        (api_data.df_play_por_genero_anio['genero'] == genero) &
        (api_data.df_play_por_genero_anio['user_id'] == usuario_maxplay_por_genero) &
        (api_data.df_play_por_genero_anio['playtime_forever'] > 0)
    ]
    # Convertimos el dataframe resultante a dict y concluimos la construcción de la respuesta del API
    df_filtrado = df_filtrado.drop(['genero', 'user_id'], axis=1).to_dict()
    respuesta_api['Horas jugadas'] = df_filtrado['playtime_forever']
    
    return respuesta_api


@app.get('/UsersRecommend/{anio}')
def UsersRecommend(anio: int):
    """Devuelve el top 3 de juegos más recomendados por usuarios para el año dado.
    """
    # Filtramos las filas donde columna 'release_year' = 'anio'
    df_maxrecommend_para_anio = api_data.df_maxrecommend_por_anio[api_data.df_maxrecommend_por_anio['release_year'] == anio]
    # Extraemos los nombre de juegos recomendados
    juegos_recommend: list = df_maxrecommend_para_anio[['app_name']].values.tolist()

    # Iteramos por la list de juegos_recommend para construir la respuesta del API
    respuesta_api = []
    for i, juego in enumerate(juegos_recommend, start=1):
        respuesta_api.append({f'Puesto {i}': juego[0]})
    # Agregamos una nota para el usuario del API en dado caso que no existen 3 juegos para el año solicitado
    if len(juegos_recommend) < 3:
        respuesta_api.append({'Nota': f'Existen {len(juegos_recommend)} juego(s) para el año {anio}.'})
    
    return respuesta_api


@app.get('/UsersNotRecommend/{anio}')
def UsersNotRecommend(anio: int):
    """Devuelve el top 3 de juegos menos recomendados por usuarios para el año dado.
    """
    # Filtramos las filas donde columna 'release_year' = 'anio'
    df_minrecommend = api_data.df_minrecommend_por_anio[api_data.df_minrecommend_por_anio['release_year'] == anio]
    # Extraemos los nombre de juegos no recomendados
    juegos_not_recommend: list = df_minrecommend[['app_name']].values.tolist()

    # Iteramos por la list de juegos_recommend para construir la respuesta del API
    respuesta_api = []
    for i, juego in enumerate(juegos_not_recommend, start=1):
        respuesta_api.append({f'Puesto {i}': juego[0]})
    # Agregamos una nota para el usuario del API en dado caso que no existen 3 juegos para el año solicitado
    if len(juegos_not_recommend) < 3:
        respuesta_api.append({'Nota': f'Existen {len(juegos_not_recommend)} juego(s) para el año {anio}.'})
    
    return respuesta_api


@app.get('/sentiment_analysis/{anio}')
def sentiment_analysis(anio: int):
    """Devuelve el conteo, por categoría, de los 3 sentiments analizados: Negativo, Neutro, Positivo,
    para el año dado.
    """
    # Guard-clause que verifica que 'anio' es una entrada válida
    if anio not in api_data.df_sentiment_anio.index:
        return (f'"{anio}" no es un año válido. '
                f'Años disponibles: de {api_data.df_sentiment_anio.index.min()} a {api_data.df_sentiment_anio.index.max()}'
        )
    # Consultamos 'df_sentiment_anio' para los valores de sentiment correspondientes a 'anio'
    respuesta_api = api_data.df_sentiment_anio.loc[anio].to_dict()

    return respuesta_api


@app.get('/recomendacion_juego/{id_producto}')
def recomendacion_juego(id_producto: str):
    """Sistema de recomendación de juegos. Devuelve los 5 juegos más
    similares/recomendados a la entrada 'id_producto'.
    """
    # Guard-clause que verifica que 'id_producto' es una entrada válida
    if id_producto not in api_data.df_similitud_coseno.index:
        return f'"{id_producto}" no es un producto válido.'
    
    # Filtramos las similitudes correspondientes a 'id_producto'
    similitud = api_data.df_similitud_coseno.loc[id_producto]
    # Ordenamos los juegos em orden descendiente basado en su similitud a 'id_producto' 
    similitud_sort = similitud.sort_values(ascending=False)

    # Extraemos los 6 juegos más similar (los 5 a retornar, más 1 siendo el mismo juego 'id_producto')
    top_juegos_similar: list = similitud_sort.iloc[:6].index.tolist()
    # Eliminamos el juego 'id_producto'
    top_juegos_similar.remove(id_producto)

    # Instanciamos un dict e iteramos la lista 'top_juegos_similar' para construir la respuesta del API
    nombres_top_juegos = {}
    for id_ in top_juegos_similar:
        # Consultamos los nombres de juegos correspondientes a sus 'id_'
        # y los almacenamos en 'nombres_top_juegos'
        nombres_top_juegos[id_] = api_data.df_id_juegos.loc[id_].iloc[0]

    nombre_producto = api_data.df_id_juegos.loc[id_producto].iloc[0]  # nombre correspondiente a 'id_producto'
    respuesta_api = {
        f'Los 5 juegos más recomendados, similares a {nombre_producto}': nombres_top_juegos
    }
    return respuesta_api