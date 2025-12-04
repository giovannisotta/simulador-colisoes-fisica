# Arquivo responsavel por lidar com a classe Bola

import random
from vpython import vector, sphere, color
import math

class Bola:
    """
    Representa uma esfera física e seu objeto gráfico 3D na simulação.

    Esta classe é responsável por:
    1. Inicializar a bola com posição e velocidade aleatórias em 3D.
    2. Atualizar a posição da bola a cada passo de tempo (integração).
    3. Tratar colisões elásticas com as paredes da caixa.
    """
    
    def __init__(self, largura, altura, profundidade, vel_max, cor, vel_min, raio, massa):
        """
        Inicializa uma nova instância da Bola com parâmetros dimensionais e físicos.

        Parâmetros:
            largura, altura, profundidade (int): Dimensões da caixa de simulação.
            vel_max, vel_min (float): Intervalo de velocidade inicial aleatória.
            cor (vpython.vector): Cor inicial do objeto gráfico.
            raio (float): Raio da esfera.
            massa (float): Massa da esfera.
        """
        
        # 1. PARÂMETROS FÍSICOS E DIMENSIONAIS
        self.massa = massa
        self.raio = raio
        self.cor = cor

        self.largura = largura
        self.altura = altura
        self.profundidade = profundidade
        
        # 2. CÁLCULO DA VELOCIDADE VETORIAL INICIAL (3D)

        # 3. POSIÇÃO E VETORES
        # Posição inicial aleatória (garantindo que o raio não ultrapasse os limites)
        self.pos = vector(random.uniform(raio,largura-raio), random.uniform(raio,altura-raio),random.uniform(raio,profundidade-raio))
        # Velocidade inical aleatória
        self.vel = vector(random.uniform(-vel_max,vel_max),random.uniform(-vel_max,vel_max),random.uniform(-vel_max,vel_max))

        # 4. OBJETO GRÁFICO (VPython)
        self.esfera_grafica = sphere(pos=self.pos, radius=self.raio, color=cor)

    def check_wall_collision(self):
        """
        Verifica e resolve a colisão elástica da esfera com as paredes.

        A lógica ajusta a posição para evitar sobreposição (tunneling) e inverte o 
        sinal do componente de velocidade relevante (Vx, Vy ou Vz).
        """
        
        # Colisão com as paredes X (Largura)
        if self.pos.x+self.raio >= self.largura:
            self.pos.x = self.largura-self.raio # Ajusta a posição para o limite
            self.vel.x *= -1                     # Inverte a componente X
        
        elif self.pos.x-self.raio <= 0:
            self.pos.x = self.raio
            self.vel.x *= -1
        
        # Colisão com as paredes Y (Altura)
        if self.pos.y+self.raio >= self.altura:
            self.pos.y = self.altura-self.raio
            self.vel.y *= -1
        
        elif self.pos.y-self.raio <= 0:
            self.pos.y = self.raio
            self.vel.y *= -1
      
        # Colisão com as paredes Z (Profundidade)
        if self.pos.z+self.raio >= self.profundidade:
            self.pos.z = self.profundidade-self.raio
            self.vel.z *= -1
        
        if self.pos.z-self.raio <= 0:
            self.pos.z = self.raio
            self.vel.z *= -1
        
        
    def update_position(self, dt):
        """
        Atualiza a posição física da bola e a posição do objeto gráfico 3D.

        Fórmula de Euler simples (integração): P_novo = P_atual + V * dt

        Parâmetros:
            dt (float): Intervalo de tempo de integração.
        """
        
        self.pos += self.vel *dt
        self.esfera_grafica.pos = self.pos
        # Atualização da cor do objeto gráfico (se a cor interna for alterada por colisão)
        self.esfera_grafica.color = self.cor