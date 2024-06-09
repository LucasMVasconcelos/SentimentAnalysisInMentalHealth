import pandas as pd
import numpy as np
def processar_dataframe(df,categoriaA,categoriaB):
    novo_dataframe = pd.DataFrame(columns=['Categoria', 'Primeiro_valor_B', 'Ultimo_valor_B', 'Mais_repetido_B'])
    categoria_anterior = None
    primeiro_valor_B = None
    ultimo_valor_B = None
    mais_repetido_B = None
    contador = 0

    for index, row in df.iterrows():
        categoria_atual = row[categoriaA]
        valor_B = row[categoriaB]
        #primeiro_index=index

        if categoria_atual != categoria_anterior:
            if contador > 0:
                novo_dataframe = pd.concat([novo_dataframe,pd.DataFrame.from_dict({'Categoria': [categoria_anterior], 
                                                        'Primeiro_valor_B': [primeiro_valor_B], 
                                                        'Ultimo_valor_B': [ultimo_valor_B], 
                                                        'Mais_repetido_B': [mais_repetido_B],
                                                        'inicio':primeiro_index})])
            primeiro_valor_B = valor_B
            primeiro_index=index
            mais_repetido_B = valor_B
            #test
            ultimo_valor_B=valor_B
            contador = 1
        else:
            ultimo_valor_B = valor_B
            contador += 1
            if contador > 1:
                contador_atual = df[(df[categoriaA] == categoria_atual) & (df[categoriaB] == valor_B)].shape[0]
                if contador_atual > contador:
                    mais_repetido_B = valor_B

        categoria_anterior = categoria_atual

    # Adicionando o último trecho ao novo DataFrame
    novo_dataframe = pd.concat([novo_dataframe,pd.DataFrame.from_dict({'Categoria': [categoria_anterior], 
                                                        'Primeiro_valor_B': [primeiro_valor_B], 
                                                        'Ultimo_valor_B': [ultimo_valor_B], 
                                                        'Mais_repetido_B': [mais_repetido_B],
                                                        'inicio':primeiro_index})])

    return novo_dataframe

def processar_dataframe_float(df,categoriaA,categoriaB):
    novo_dataframe = pd.DataFrame(columns=['Categoria', 'Primeiro_valor_B', 'Ultimo_valor_B','Media_B','inicio'])
    categoria_anterior = None
    primeiro_valor_B = None
    ultimo_valor_B = None
    media_B = None
    contador = 0
    soma_valores_B = 0

    for index, row in df.iterrows():
        categoria_atual = row[categoriaA]
        valor_B = row[categoriaB]
        if categoria_atual != categoria_anterior:
            if contador > 0:
                a=(soma_valores_B/ (contador+1))
                media_B = soma_valores_B / (contador)
                novo_dataframe = pd.concat([novo_dataframe,pd.DataFrame.from_dict({'Categoria': [categoria_anterior], 
                                                        'Primeiro_valor_B': [primeiro_valor_B], 
                                                        'Ultimo_valor_B': [ultimo_valor_B], 
                                                        'Media_B': [media_B],
                                                        'inicio':primeiro_index})])
            primeiro_valor_B = valor_B
            primeiro_index=index
            soma_valores_B = valor_B
            #test
            ultimo_valor_B=valor_B
            contador = 1
        else:
            ultimo_valor_B = valor_B
            contador += 1
            soma_valores_B += valor_B

        categoria_anterior = categoria_atual
    media_B = soma_valores_B / (contador)
    # Adicionando o último trecho ao novo DataFrame
    novo_dataframe = pd.concat([novo_dataframe,pd.DataFrame.from_dict({'Categoria': [categoria_anterior], 
                                                        'Primeiro_valor_B': [primeiro_valor_B], 
                                                        'Ultimo_valor_B': [ultimo_valor_B], 
                                                        'Media_B': [media_B],
                                                        'inicio':primeiro_index})])

    return novo_dataframe