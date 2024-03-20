# Proyecto MLOps con Dataset de Steam

## Descripción
Este proyecto tiene como objetivo implementar un flujo de trabajo completo de MLOps utilizando el dataset de Steam. Steam es la plataforma líder en distribución digital de videojuegos, y su dataset refleja las preferencias y comportamientos de millones de jugadores alrededor del mundo. El dataset utilizado incluye datos como género, desarrollador, métricas de horas jugadas y reseñas, entre otras. Este proyecto divide en tres partes principales: ETL (Extract, Transform, Load), EDA (Exploratory Data Analysis) y la creación de una API para proporcionar acceso a la información procesada.

## ETL
El proceso ETL se encarga de extraer los datos del dataset de Steam, transformarlos según sea necesario y que facilite el análisis y la operación del API y modelos de Machine Learning.

## EDA
El análisis exploratorio de datos nos permite comprender mejor el dataset, identificar patrones, anomalías en el dataset de Steam.

### Técnicas Utilizadas
- Visualización de nubes de palabras
- Análisis de correlación


### Librerías Utilizadas
- matplotlib 
- seaborn
- wordcloud 


## API
La API proporciona una interfaz para solicitar datos puntuales del dataset.

### Endpoints
- `/PlayTimeGenre/{genero}`: Devuelve el año con más horas jugadas para dicho género.
- `/UserForGenre/{genero}`: Devuelve el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año.
- `/UsersRecommend/{anio}`: Devuelve el top 3 de juegos más recomendados por usuarios para el año dado.
- `/UsersNotRecommend/{anio}`: Devuelve el top 3 de juegos menos recomendados por usuarios para el año dado.
- `/sentiment_analysis/{anio}`: Devuelve el conteo, por categoría, de los 3 sentiments analizados: Negativo, Neutro, Positivo,
    para el año dado.
- `/recomendacion_juego/{id_producto}`: Sistema de recomendación de juegos. Devuelve los 5 juegos más
    similares/recomendados a la entrada 'id_producto'.

### Tecnologías
- Framework de la API: FastAPI
- ASGI web server: Uvicorn

## Enlaces
- API: https://a.com:5000/docs
- Video explicativo del proyecto: https://a.com