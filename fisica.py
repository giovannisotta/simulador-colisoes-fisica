from ball import Bola
from vpython import vector, mag2, dot, cross, color
from math import sqrt


# Confirma se ouve ou nao colisão entre duas bolas
def verifica_colisao(b1: Bola, b2: Bola) -> bool:
    # armazena o vetor normal/distancia entre as duas bolas
    n = b1.pos-b2.pos
    
    # armazena a magnitude ao quadrado do vetor n utilizando o método mag2 para vetores da biblioteca vpython
    d_quadrada = n.mag2

    # Impede casos de divisão por zero e de casos onde as bolas inicializam na mesma posição
    if d_quadrada == 0:
        return False


    soma_raios_quadrado = (b1.raio + b2.raio)**2

    # retorna True se houver colisão ou False se não houver colisão
    return d_quadrada <= soma_raios_quadrado


def resolve_colisao_elastica(b1: Bola, b2: Bola):

    """
    Esta função implementa o método vetorial (sem trigonometria) para colisões elásticas, 
    garantindo a conservação do Momento e da Energia Cinética.

    LÓGICA:
    1. CHECAGEM: Verifica se há sobreposição (overlap) e se as bolas estão se aproximando 
    (velocidade relativa > 0 na direção Normal).
    2. POSIÇÃO: Resolve o overlap (sobreposição) ajustando as posições das bolas para que 
    fiquem exatamente tangentes.
    3. DECOMPOSIÇÃO: Decompõe a velocidade total em componentes Normal (linha de impacto) 
    e Tangencial (perpendicular à linha de impacto).
    4. RESOLUÇÃO: Aplica a fórmula de colisão 1D apenas à componente Normal, que é a única 
    que sofre alteração de velocidade. A componente Tangencial é conservada.
    5. RECOMPOSIÇÃO: Soma os novos vetores Normal e Tangencial para obter a nova velocidade 
    vetorial final de cada esfera.
    """

    n = b2.pos - b1.pos # n é o vetor Normal (linha de impacto)
    
    # 1. VERIFICAÇÃO DE COLISÃO E SENTIDO (Pré-colisão)
    # ----------------------------------------------------------------------------------
    # Encontra a distância ao quadrado (d²) e a soma dos raios ao quadrado (R²).
    distancia_sq = n.mag2
    soma_raios_sq = (b1.raio + b2.raio)**2
    
    # Sai se a distância for zero (mesma posição) ou se não houver sobreposição (d² > R²).
    if distancia_sq == 0 or distancia_sq > soma_raios_sq:
        return
    
    # Vetor Unitário Normal (un): Usado para projetar as velocidades.
    un = n.hat
    v_rel = b1.vel - b2.vel 
    
    # 2. CHECAGEM DE APROXIMAÇÃO
    # ----------------------------------------------------------------------------------
    # Produto Escalar (dot product) para verificar a velocidade de aproximação
    # (Projeta a velocidade relativa no vetor normal).
    velocidade_de_aproximacao = v_rel.dot(un) 
    
    # Se <= 0, as bolas já estão se separando; a colisão já foi resolvida (ou estão tangentes).
    if velocidade_de_aproximacao <= 0:
        return
        
    # 3. AJUSTE DE POSIÇÃO (Resolução da Sobreposição)
    # ----------------------------------------------------------------------------------
    # Calcula o overlap: Sobreposicao = Distância_Real (R) - Soma_Raios (d).
    # Usando sqrt(R²) - sqrt(d²) para obter R - d.
    sobreposicao = sqrt(soma_raios_sq) - sqrt(distancia_sq)
    ajuste_posicao = un * (sobreposicao / 2.0)

    # Move as esferas para que fiquem exatamente tangentes, corrigindo o overlap.
    b1.pos -= ajuste_posicao 
    b2.pos += ajuste_posicao
    
    # 4. DECOMPOSIÇÃO DE VELOCIDADE (Componentes Escalados)
    # ----------------------------------------------------------------------------------
    # Projeta as velocidades (v1 e v2) nos vetores Normal (un) para obter as velocidades escalares
    # na direção Normal (v1n e v2n).
    v1n = b1.vel.dot(un)
    v2n = b2.vel.dot(un)
    
    m1 = b1.massa
    m2 = b2.massa

    # 5. CÁLCULO DAS NOVAS VELOCIDADES NORMAIS (Colisão 1D)
    # ----------------------------------------------------------------------------------
    # Aplica as fórmulas de colisão elástica unidimensional.
    v1n_prime = (v1n * (m1 - m2) + 2 * m2 * v2n) / (m1 + m2)
    v2n_prime = (v2n * (m2 - m1) + 2 * m1 * v1n) / (m1 + m2)

    # 6. RECOMPOSIÇÃO DOS VETORES
    # ----------------------------------------------------------------------------------
    # Componente Normal: Multiplica a nova velocidade escalar pelo Vetor Unitário Normal.
    v1n_vec = v1n_prime * un
    v2n_vec = v2n_prime * un

    # Componente Tangencial: É conservada (não muda).
    # O componente Tangencial (vetorial) é obtido subtraindo a componente Normal (vetorial) da velocidade total.
    v1t_vec = b1.vel - v1n * un
    v2t_vec = b2.vel - v2n * un
    
    # 7. VELOCIDADE FINAL
    # ----------------------------------------------------------------------------------
    # A nova velocidade final é a soma das componentes Normal e Tangencial (vetoriais).
    b1.vel = v1n_vec + v1t_vec
    b2.vel = v2n_vec + v2t_vec
    
    # 8. FEEDBACK VISUAL
    # ----------------------------------------------------------------------------------
    # Muda a cor do objeto gráfico para dar feedback de que a colisão ocorreu.
    b1.esfera_grafica.color = color.red
    b2.esfera_grafica.color = color.red


def calcular_metricas_conservacao(lista_bolas: list[Bola]) -> tuple[vector, float]:
    # Vetor do momento linear total    
    p_total = vector(0,0,0)
    # Variavel que armazena a Energia cinética total
    ke = 0
    # Percorre a lista de bolas somando o momento linear na variavel p_total e somando a energia cinetica na variavel ke 
    for b in lista_bolas:
        p_total += b.massa*b.vel
        ke += b.massa*b.vel.mag2*0.5
    
    # Armazena as duas variáveis numa tupla e retorna elas na função
    metricas_conservacao = (p_total,ke) 
    return metricas_conservacao

     



    

    


    






