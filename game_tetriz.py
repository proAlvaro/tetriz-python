import pygame
import random

# Configurações do jogo
largura_tela = 800
altura_tela = 600
largura_tabela = 10
altura_tabela = 20
tamanho_quadrado = 30
velocidade_queda = 500  # Velocidade de queda dos blocos em milissegundos (quanto maior, mais devagar)

# Cores
cores = [
    (0, 0, 0),
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (255, 165, 0),
    (128, 0, 128),
]

# Formas das peças
formas = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 1], [0, 1, 0]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 0], [0, 1, 1]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 1], [0, 0, 1]],
]

class Tetris:
    def __init__(self):
        self.tabela = [[0 for _ in range(largura_tabela)] for _ in range(altura_tabela)]
        self.atual_peca = self.nova_peca()
        self.proxima_peca = self.nova_peca()
        self.linhas_completadas = 0
        self.pontuacao = 0
        self.offset_x = largura_tabela // 2
        self.offset_y = 0
        self.tempo_queda = 0
        self.ultima_atualizacao = pygame.time.get_ticks()

    def nova_peca(self):
        return [random.choice(formas), random.choice(cores)]

    def valida_posicao(self, peca, deslocamento):
        offset_x, offset_y = deslocamento
        for y, linha in enumerate(peca):
            for x, valor in enumerate(linha):
                if valor:
                    if x + offset_x < 0 or x + offset_x >= largura_tabela or y + offset_y >= altura_tabela:
                        return False
                    if y + offset_y >= 0 and self.tabela[y + offset_y][x + offset_x]:
                        return False
        return True

    def fixar_peca(self):
        for y, linha in enumerate(self.atual_peca[0]):
            for x, valor in enumerate(linha):
                if valor and y + self.offset_y >= 0:
                    self.tabela[y + self.offset_y][x + self.offset_x] = self.atual_peca[1]
        self.remover_linhas()
        self.atual_peca = self.proxima_peca
        self.proxima_peca = self.nova_peca()
        self.offset_x = largura_tabela // 2
        self.offset_y = 0
        if not self.valida_posicao(self.atual_peca[0], (self.offset_x, self.offset_y)):
            self.game_over()

    def remover_linhas(self):
        linhas_a_remover = [i for i, linha in enumerate(self.tabela) if 0 not in linha]
        for i in linhas_a_remover:
            del self.tabela[i]
            self.tabela.insert(0, [0 for _ in range(largura_tabela)])
        self.linhas_completadas += len(linhas_a_remover)
        self.pontuacao += len(linhas_a_remover) * 100

    def game_over(self):
        self.tabela = [[0 for _ in range(largura_tabela)] for _ in range(altura_tabela)]
        self.linhas_completadas = 0
        self.pontuacao = 0
        self.atual_peca = self.nova_peca()
        self.proxima_peca = self.nova_peca()
        self.offset_x = largura_tabela // 2
        self.offset_y = 0

    def rotacionar_peca(self):
        peca_rotacionada = [list(linha) for linha in zip(*self.atual_peca[0][::-1])]
        if self.valida_posicao(peca_rotacionada, (self.offset_x, self.offset_y)):
            self.atual_peca[0] = peca_rotacionada

    def desenhar_tela(self, tela):
        tela.fill((0, 0, 0))
        # Desenha bordas
        pygame.draw.rect(tela, (255, 255, 255), (0, 0, largura_tabela * tamanho_quadrado, altura_tabela * tamanho_quadrado), 2)
        pygame.draw.line(tela, (255, 255, 255), (0, 0), (0, altura_tabela * tamanho_quadrado), 2)
        pygame.draw.line(tela, (255, 255, 255), (largura_tabela * tamanho_quadrado, 0), (largura_tabela * tamanho_quadrado, altura_tabela * tamanho_quadrado), 2)
        for y, linha in enumerate(self.tabela):
            for x, cor in enumerate(linha):
                pygame.draw.rect(tela, cor, (x * tamanho_quadrado, y * tamanho_quadrado, tamanho_quadrado, tamanho_quadrado))
        for y, linha in enumerate(self.atual_peca[0]):
            for x, valor in enumerate(linha):
                if valor:
                    pygame.draw.rect(tela, self.atual_peca[1], ((x + self.offset_x) * tamanho_quadrado, (y + self.offset_y) * tamanho_quadrado, tamanho_quadrado, tamanho_quadrado))
        # Desenha a próxima peça
        self.desenhar_proxima_peca(tela)
        # Desenha a pontuação
        self.desenhar_pontuacao(tela)

    def desenhar_proxima_peca(self, tela):
        for y, linha in enumerate(self.proxima_peca[0]):
            for x, valor in enumerate(linha):
                if valor:
                    pygame.draw.rect(tela, self.proxima_peca[1], ((x + largura_tabela + 1) * tamanho_quadrado, (y + 1) * tamanho_quadrado, tamanho_quadrado, tamanho_quadrado))

    def desenhar_pontuacao(self, tela):
        fonte = pygame.font.SysFont('Arial', 25)
        texto = fonte.render(f"Pontuação: {self.pontuacao}", True, (255, 255, 255))
        tela.blit(texto, (largura_tabela * tamanho_quadrado + 20, 5))

def main():
    pygame.init()
    tela = pygame.display.set_mode((largura_tela, altura_tela))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()
    jogo = Tetris()
    rodando = True

    while rodando:
        tempo_atual = pygame.time.get_ticks()
        jogo.tempo_queda += tempo_atual - jogo.ultima_atualizacao
        jogo.ultima_atualizacao = tempo_atual

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    jogo.rotacionar_peca()
                elif evento.key == pygame.K_DOWN:
                    jogo.offset_y += 1
                    if not jogo.valida_posicao(jogo.atual_peca[0], (jogo.offset_x, jogo.offset_y)):
                        jogo.offset_y -= 1
                        jogo.fixar_peca()
                elif evento.key == pygame.K_LEFT:
                    jogo.offset_x -= 1
                    if not jogo.valida_posicao(jogo.atual_peca[0], (jogo.offset_x, jogo.offset_y)):
                        jogo.offset_x += 1
                elif evento.key == pygame.K_RIGHT:
                    jogo.offset_x += 1
                    if not jogo.valida_posicao(jogo.atual_peca[0], (jogo.offset_x, jogo.offset_y)):
                        jogo.offset_x -= 1

        if jogo.tempo_queda >= velocidade_queda:
            jogo.tempo_queda = 0
            jogo.offset_y += 1
            if not jogo.valida_posicao(jogo.atual_peca[0], (jogo.offset_x, jogo.offset_y)):
                jogo.offset_y -= 1
                jogo.fixar_peca()

        jogo.desenhar_tela(tela)
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()