import json
from vpython import scene, box, color, vector, rate # Importa todas as ferramentas gráficas 3D
from ball import Bola # Sua classe Bola deve usar agora vpython.vector ou Vector3
import fisica

def carregar_config(arquivo="config.json"):
    try:
        with open(arquivo, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Erro Crítico: Arquivo de configuração '{arquivo}' não encontrado.")
        print("Certifique-se de que 'config.json' está na mesma pasta do 'main.py'.")
        exit()

# Carrega todas as configurações
CONFIG = carregar_config()

# CORES PADRAO
# Parâmetros de Dimensão
LARGURA = CONFIG['DIMENSOES']['LARGURA']
ALTURA = CONFIG['DIMENSOES']['ALTURA']
PROFUNDIDADE = CONFIG['DIMENSOES']['PROFUNDIDADE']

# Parâmetros de Física
VEL_MAX = CONFIG['FISICA']['VEL_MAX']
VEL_MIN = CONFIG['FISICA']['VEL_MIN']
RAIO_PADRAO = CONFIG['FISICA']['RAIO_PADRAO']
NUM_BOLAS = CONFIG['FISICA']['NUM_BOLAS']
EPSILON = CONFIG['FISICA']['EPSILON']
MASSA_PADRAO = CONFIG['FISICA']['MASSA_PADRAO']

# Parâmetros de Tempo
FPS = CONFIG['TEMPO']['FPS']
DT = 1.0 / FPS # DT é calculado com base no FPS lido

# --- SETUP DO AMBIENTE VPYTHON ---
scene.width = 1920
scene.height = 1080
scene.title = "Simulação de Colisões Elásticas 3D"
scene.background = color.gray(0.5)

# Desenha a caixa de limites visuais (opacidade 0.1 para que o interior seja visível)
box(pos=vector(LARGURA/2, ALTURA/2, PROFUNDIDADE/2), 
    size=vector(LARGURA, ALTURA, PROFUNDIDADE), 
    color=color.black, opacity=0.1) 
    
# Posiciona a câmera para ver a cena toda
scene.camera.pos = vector(LARGURA/2, ALTURA/2, -PROFUNDIDADE)

scene.center = vector(LARGURA/2, ALTURA/2, PROFUNDIDADE/2)
# --- CRIAÇÃO DE OBJETOS ---
lista_de_bolas = []

for _ in range(NUM_BOLAS):
    nova_bola = Bola(LARGURA, ALTURA, PROFUNDIDADE, VEL_MAX,color.white, VEL_MIN, RAIO_PADRAO,MASSA_PADRAO)
    lista_de_bolas.append(nova_bola)


while True:
    rate(FPS) # Controla a taxa de execução

    momento_inicial, ki = fisica.calcular_metricas_conservacao(lista_de_bolas)
    # 1. ATUALIZAÇÃO E COLISÕES
    for bola1 in lista_de_bolas:
        # Move a bola (o update_position também atualiza o objeto gráfico)
        bola1.update_position(DT) 
        
        # Checa e resolve a colisão com as 6 paredes (agora com lógica Z)
        bola1.check_wall_collision() 
        
        for bola2 in lista_de_bolas:
            if fisica.verifica_colisao(bola1,bola2):
                fisica.resolve_colisao_elastica(bola1, bola2)
        
    momento_final, kf = fisica.calcular_metricas_conservacao(lista_de_bolas)
    dk = abs(kf-ki)
    if dk > EPSILON:
        print("NAO CONSERVOU")

