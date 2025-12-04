from ball import Bola
from vpython import vector, mag2, dot, cross, color
from math import sqrt



def verifica_colisao(b1: Bola, b2: Bola) -> bool:
    n = b1.pos-b2.pos
    
    d_quadrada = n.mag2

    if d_quadrada == 0:
        return False

    soma_raios_quadrado = (b1.raio + b2.raio)**2

    return d_quadrada <= soma_raios_quadrado

def resolve_colisao_elastica(b1: Bola, b2: Bola):

    n = b2.pos - b1.pos
    vetor_acima = vector(0, 1, 0)
    
    # 1. Checagem de Colisão (Overlap)
    distancia_sq = n.mag2
    soma_raios_sq = (b1.raio + b2.raio)**2
    
    if distancia_sq == 0 or distancia_sq > soma_raios_sq:
        return
    
    # --- NOVO PONTO DE VERIFICAÇÃO ---
    v_rel = b1.vel - b2.vel 
    un = n.hat
    
    # 2. PRODUTO ESCALAR E CHECAGEM DE APROXIMAÇÃO (DEVE VIR ANTES DO AJUSTE DE POSIÇÃO!)
    velocidade_de_aproximacao = v_rel.dot(un) 
    
    # Se a velocidade de aproximação for negativa ou zero, as bolas estão se separando.
    # NÃO aplique física de colisão se elas já estiverem se separando!
    if velocidade_de_aproximacao <= 0:
        return
        
    # 3. CÁLCULO E AJUSTE DA SOBREPOSIÇÃO (CORRETO)
    sobreposicao = sqrt(soma_raios_sq) - sqrt(distancia_sq)
    ajuste_posicao = un * (sobreposicao / 2.0)

    b1.pos -= ajuste_posicao 
    b2.pos += ajuste_posicao
    
    # ---------------------------------
    
    # 4. RESOLUÇÃO DA VELOCIDADE (O restante da lógica é para a conservação da energia/momento)
    v1n = b1.vel.dot(un)
    v2n = b2.vel.dot(un)
    
    m1 = b1.massa
    m2 = b2.massa

    v1n_prime = (v1n * (m1 - m2) + 2 * m2 * v2n) / (m1 + m2)
    v2n_prime = (v2n * (m2 - m1) + 2 * m1 * v1n) / (m1 + m2)

    v1n_vec = v1n_prime * un
    v2n_vec = v2n_prime * un

    ut = un.cross(vetor_acima) # Recompute ut if needed, though usually OK here

    # Tangencial (deve ser conservada)
    v1t_vec = (b1.vel - v1n * un) # Melhor forma de calcular v_tangencial é subtrair a componente normal
    v2t_vec = (b2.vel - v2n * un)
    
    b1.vel = v1n_vec + v1t_vec
    b2.vel = v2n_vec + v2t_vec
    
    # 5. CORREÇÃO DA COR (use o objeto gráfico para ter efeito visual)
    b1.esfera_grafica.color = color.red
    b2.esfera_grafica.color = color.red
    
def calcular_metricas_conservacao(lista_bolas: list[Bola]) -> tuple[vector, float]:
    
    p_total = vector(0,0,0)
    ke = 0

    for b in lista_bolas:
        p_total += b.massa*b.vel
        ke += b.massa*b.vel.mag2*0.5
    
    metricas_conservacao = (p_total,ke)
    return metricas_conservacao

     



    

    


    






