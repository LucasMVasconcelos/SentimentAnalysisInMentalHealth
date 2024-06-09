import pandas as pd
import numpy as np
from scipy import stats

def coluna_min_value(row):
    # Encontre o nome da coluna com o valor máximo
    min_value = row.min()
    return min_value
    
def coluna_max_value(row):
    # Encontre o nome da coluna com o valor máximo
    max_value = row.max()
    return max_value

def windowed_cross_correlation(df, col1, col2, window_size,winc=2,lag=1):
    """
    Perform windowed cross-correlation between two columns of a DataFrame.

    Parameters:
    - df: pandas DataFrame
    - col1: str, the name of the first column
    - col2: str, the name of the second column
    - window_size: int, size of the window for the cross-correlation

    Returns:
    - result_df: pandas DataFrame with windowed cross-correlation values
    """
    # Ensure the specified columns exist in the DataFrame
    if col1 not in df.columns or col2 not in df.columns:
        raise ValueError("Specified columns not found in the DataFrame")
    # Calculate cross-correlation for each window
    cross_correlation_values = []
    index=0
    combinations=lag*2+1
    dict={}
    for columns in [n for n in range(-lag,lag+1,1)]:
        dict[columns]=[]
    for index_inc in range(0,df.shape[0],winc):
        start_one=winc+index_inc
        for i in range(-lag,lag+1,1):
            if start_one+window_size<=df.shape[0]:
                if i<=0:
                    window1 = df[col1].iloc[start_one:start_one+window_size].values
                    window2 = df[col2].iloc[start_one+i:start_one+i+window_size].values
                    cross_corr=stats.pearsonr(window1, window2)
                    dict[i].append(cross_corr[0])
                else:
                    window1 = df[col1].iloc[start_one-i:start_one+window_size-i].values
                    window2 = df[col2].iloc[start_one:start_one+window_size].values
                    #print(index_inc,len(window1),len(window2))
                    cross_corr=stats.pearsonr(window1, window2)
                    dict[i].append(cross_corr[0])
            else:
                z=1
    result_df = pd.DataFrame(dict)
    result_df["max_value"]=result_df.loc[:, result_df.columns].apply(coluna_max_value, axis=1)
    result_df["min_value"]=result_df.loc[:, result_df.columns].apply(coluna_min_value, axis=1)

    return result_df

def transformar_em_dummy(dataframe, coluna):
    # Iterar sobre as linhas do DataFrame
    categorias=dataframe[coluna].unique()
    for indice, linha in dataframe.iterrows():
        # Iterar sobre os valores na linha
        for item in categorias:
            if linha[coluna]==item:
                dataframe[f"{coluna}_{item}"]=1
            else:
                dataframe[f"{coluna}_{item}"]=0
            # Criar uma nova coluna com o nome do valor e atribuir 1 se for igual ao valor atual, 0 caso contrário
    
    # Preencher valores NaN com 0
    #dataframe.fillna(0, inplace=True)
    
    return dataframe

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


def needleman_wunsch(seq1, seq2, match_score=1, mismatch_score=-1, gap_penalty=-1):
    # Inicialização da matriz de pontuação
    rows = len(seq1) + 1
    cols = len(seq2) + 1
    score_matrix = [[0] * cols for _ in range(rows)]

    # Inicialização das primeiras linhas e colunas com penalidades de lacuna
    for i in range(1, rows):
        score_matrix[i][0] = i * gap_penalty
    for j in range(1, cols):
        score_matrix[0][j] = j * gap_penalty

    # Preenchimento da matriz de pontuação
    for i in range(1, rows):
        for j in range(1, cols):
            match = score_matrix[i - 1][j - 1] + (match_score if seq1[i - 1] == seq2[j - 1] else mismatch_score)
            delete = score_matrix[i - 1][j] + gap_penalty
            insert = score_matrix[i][j - 1] + gap_penalty
            score_matrix[i][j] = max(match, delete, insert)



    # Recuperação do alinhamento
    align1 = ''
    align2 = ''
    i, j = rows - 1, cols - 1
    while i > 0 and j > 0:
        if score_matrix[i][j] == score_matrix[i - 1][j - 1] + (match_score if seq1[i - 1] == seq2[j - 1] else mismatch_score):
            align1 = seq1[i - 1] + align1
            align2 = seq2[j - 1] + align2
            i -= 1
            j -= 1
        elif score_matrix[i][j] == score_matrix[i - 1][j] + gap_penalty:
            align1 = seq1[i - 1] + align1
            align2 = '-' + align2
            i -= 1
        else:
            align1 = '-' + align1
            align2 = seq2[j - 1] + align2
            j -= 1

    while i > 0:
        align1 = seq1[i - 1] + align1
        align2 = '-' + align2
        i -= 1
    while j > 0:
        align1 = '-' + align1
        align2 = seq2[j - 1] + align2
        j -= 1

    return alignment_score, align1, align2

def needleman_wunsch_matriz(seq1, seq2, gap, substitution_matrix=None):
    # Inicialização da matriz de pontuação
    n = len(seq1)
    m = len(seq2)
    score_matrix = [[0 for j in range(m + 1)] for i in range(n + 1)]

    # Inicialização da primeira linha e primeira coluna
    for i in range(1, n + 1):
        score_matrix[i][0] = i * gap
    for j in range(1, m + 1):
        score_matrix[0][j] = j * gap

    # Preenchimento da matriz de pontuação
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            value=substitution_matrix.get((seq1[i - 1], seq2[j - 1]), -1)
            match = score_matrix[i - 1][j - 1] + value
            delete = score_matrix[i - 1][j] + gap
            insert = score_matrix[i][j - 1] + gap
            score_matrix[i][j] = max(match, delete, insert)
    # Recuperação do escore do alinhamento ótimo
    alignment_score = score_matrix[-1][-1]
    return alignment_score,np.array(score_matrix).max()