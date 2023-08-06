import numpy as np
from mmq import metodo_minimos_quadrados

def hurst(dados: np.array, tipo: str = "pow2") -> float:

    """
    :param dados: Este parâmetro deve estar estruturado como um array
    :param tipo: Este parâmetro deve ser uma string. As opções são "pow2" e "incremental".
    :return: O retorno deverá ser o coeficiente angular da reta média de dados logaritmizados (entropizados)
    """

    binario = list(bin(len(dados)).replace("0b", ""))
    binario[1:] = "0" * (len(binario) - 1)
    closest_2_pow = int("".join(binario), 2)

    if tipo == "pow2":
        l = [2 ** i for i in range(2, int(np.log2(closest_2_pow)) + 1, 1)]
        l.append(len(dados))
    elif tipo == "incremental":
        l = range(2, len(dados) + 1)
    else:
        raise ValueError("Tipo de cálculo não reconhecido. Escolha entre 'pow2' e 'incremental'.")
    
    serie1 = np.zeros(len(l))
    serie2 = np.zeros(len(l))
    for i, tamanho in enumerate(l):
        serie_aux = dados[:tamanho]
        
        media = np.mean(serie_aux)
        y = [0]
        for j, el in enumerate(serie_aux[1:]):
            y.append(y[j] + el - media)
        
        y_max = np.max(y)
        y_min = np.min(y)

        std = np.std(serie_aux)

        if std != 0 and y_max != y_min:
            serie1[i] = np.log2(tamanho)
            serie2[i] = np.log2((y_max - y_min) / std)
            
        
    coef_ang = metodo_minimos_quadrados.mmq(serie1, serie2, g=1)[0]

    return coef_ang

if __name__ == "__main__":
    dados = np.random.normal(0, 1, 100000)
    print(hurst(dados, tipo="pow2"))
