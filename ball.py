import random
from vpython import vector, sphere, color
import math
import json

class Bola:
    def __init__(self, largura, altura, profundidade, vel_max, cor, vel_min, raio, massa):
        
        self.massa = massa
        self.raio = raio
        self.cor = cor

        self.largura = largura
        self.altura = altura
        self.profundidade = profundidade
        
        vel = random.uniform(vel_min, vel_max)

        # 2. Geração dos Ângulos (em radianos)
        theta = random.uniform(0, math.pi)       # Ângulo Polar
        phi = random.uniform(0, 2 * math.pi)     # Ângulo Azimutal

        vel_x = vel * math.sin(theta) * math.cos(phi)
        vel_y = vel * math.sin(theta) * math.sin(phi)
        vel_z = vel * math.cos(theta)

        self.pos = vector(random.uniform(raio,largura-raio), random.uniform(raio,altura-raio),random.uniform(raio,profundidade-raio))
        self.vel = vector(vel_x, vel_y, vel_z)

        self.esfera_grafica = sphere(pos=self.pos, radius=self.raio, color=cor)

    def check_wall_collision(self):
        if self.pos.x+self.raio >= self.largura:
            self.pos.x = self.largura-self.raio
            self.vel.x *= -1
        
        elif self.pos.x-self.raio <= 0:
            self.pos.x = self.raio
            self.vel.x *= -1
        
        if self.pos.y+self.raio >= self.altura:
            self.pos.y = self.altura-self.raio
            self.vel.y *= -1
        
        elif self.pos.y-self.raio <= 0:
            self.pos.y = self.raio
            self.vel.y *= -1
      

        if self.pos.z+self.raio >= self.profundidade:
            self.pos.z = self.profundidade-self.raio
            self.vel.z *= -1
        
        if self.pos.z-self.raio <= 0:
            self.pos.z = self.raio
            self.vel.z *= -1
        
        
    def update_position(self, dt):
        
        self.pos += self.vel *dt
        self.esfera_grafica.pos = self.pos
        self.esfera_grafica.color = self.cor

    

