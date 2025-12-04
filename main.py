import json # Importa o arquivo json
from vpython import scene, box, color, vector, rate 
from ball import Bola # Importa a classe Bola
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
RAIO_PADRAO = CONFIG['FISICA']['RAIO_PADRAO']
NUM_BOLAS = CONFIG['FISICA']['NUM_BOLAS']
MASSA_PADRAO = CONFIG['FISICA']['MASSA_PADRAO']

# Parâmetros de Tempo
FPS = CONFIG['TEMPO']['FPS']
DT = 1.0 / FPS # DT é calculado com base no FPS lido

# --- SETUP DO AMBIENTE VPYTHON ---
scene.width = CONFIG['TELA']['WIDTH']
scene.height = CONFIG['TELA']['HEIGHT']
scene.title = CONFIG['TELA']['TITLE']
scene.background = color.gray(0.5)

# Desenha a caixa de limites visuais (opacidade 0.1 para que o interior seja visível)
box(pos=vector(LARGURA/2, ALTURA/2, PROFUNDIDADE/2), 
    size=vector(LARGURA, ALTURA, PROFUNDIDADE), 
    color=color.black, opacity=0.1) 
    
# Posiciona a câmera para ver a cena toda
scene.camera.pos = vector(LARGURA/2, ALTURA/2, -PROFUNDIDADE)
# Posiciona o centro da câmera no centro da caixa
scene.center = vector(LARGURA/2, ALTURA/2, PROFUNDIDADE/2)

# Cria a lista de bolas, inicializando 'NUM_BOLAS' objetos Bola 
# com parâmetros e posições padrões do arquivo config.json.
lista_de_bolas = [Bola(LARGURA, ALTURA, PROFUNDIDADE, VEL_MAX,color.white, RAIO_PADRAO,MASSA_PADRAO) 
                  for _ in range(NUM_BOLAS)]

#Loop principal
while True:
    rate(FPS) # Controla a taxa de execução

    #ATUALIZAÇÃO E COLISÕES
    #Percorre a lista de bolas
    for bola1 in lista_de_bolas:
        # Atualiza a poisção atual da bola e o obejeto grafico
        bola1.update_position(DT) 
        
        # Checa e resolve a colisão com as paredes
        bola1.check_wall_collision() 
        
        #Percorre a lista de bolas uma segunda vez para cada bola
        for bola2 in lista_de_bolas:
            if fisica.verifica_colisao(bola1,bola2):
                #Calcula as novas velocidade das bolas após as colisões
                fisica.resolve_colisao_elastica(bola1, bola2)
        


