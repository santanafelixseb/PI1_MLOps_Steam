import pandas as pd


"""Carga de datos para uso en el API.
"""

# Función: PlayTimeGenre
df_generos_year_playtime = pd.read_pickle('./data_api/df_generos_year_playtime.pkl')

# Función: UserForGenre
df_maxplay_por_genero = pd.read_pickle('./data_api/df_maxplay_por_genero.pkl')
df_play_por_genero_anio = pd.read_pickle('./data_api/df_play_por_genero_por_anio.pkl')

# Función: UsersRecommend
df_maxrecommend_por_anio = pd.read_pickle(f'./data_api/df_maxrecommend_por_anio.pkl')

# Función: UsersNotRecommend
df_minrecommend_por_anio = pd.read_pickle(f'./data_api/df_minrecommend_por_anio.pkl')

# Función: sentiment_analysis
df_sentiment_anio = pd.read_pickle(f'./data_api/df_sentiment_por_anio.pkl')

# Función: recomendacion_juego
df_similitud_coseno = pd.read_pickle(f'./data_api/df_similitud_coseno.pkl')
df_id_juegos = pd.read_pickle(f'./data_api/df_id_juegos.pkl')