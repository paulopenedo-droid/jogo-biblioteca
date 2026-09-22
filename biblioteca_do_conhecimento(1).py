# Escreva o seu código aqui :-)import pygame
import sys

# ==========================================================
# A BIBLIOTECA DO CONHECIMENTO
# Projeto de Pensamento Computacional - UFMS
# Versão 1.0 - protótipo gráfico
#
# Controles:
# Setas ou WASD = movimentar o avatar
# E = interagir com personagens/objetos
# ENTER = confirmar resposta
# 1, 2 ou 3 = escolher resposta
# ESC = sair
# ==========================================================

pygame.init()

LARGURA = 1000
ALTURA = 650
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("A Biblioteca do Conhecimento")

RELOGIO = pygame.time.Clock()

# Cores
FUNDO = (238, 230, 214)
PAREDE = (222, 210, 188)
MADEIRA = (128, 82, 48)
MADEIRA_CLARA = (166, 112, 70)
VERDE = (67, 125, 82)
AZUL = (63, 105, 160)
AMARELO = (235, 190, 60)
BRANCO = (255, 255, 255)
PRETO = (30, 30, 30)
CINZA = (100, 100, 100)
VERMELHO = (180, 65, 65)
ROXO = (115, 80, 150)

fonte = pygame.font.SysFont("arial", 22)
fonte_pequena = pygame.font.SysFont("arial", 18)
fonte_grande = pygame.font.SysFont("arial", 32, bold=True)
fonte_titulo = pygame.font.SysFont("arial", 42, bold=True)

# ----------------------------------------------------------
# Estado do jogo
# ----------------------------------------------------------

pontos = 0
nivel = 1
recompensas = []
nome = "Aluno"

mensagem = "Explore a biblioteca! Aproxime-se de um personagem ou objeto e pressione E."
modo = "jogo"

pergunta_atual = 0
resposta_selecionada = None
perguntas_respondidas = set()

livro_encontrado = False
missao_finalizada = False

# ----------------------------------------------------------
# Objetos do cenário
# ----------------------------------------------------------

avatar = pygame.Rect(110, 500, 34, 44)
velocidade = 4

professora = pygame.Rect(200, 170, 40, 50)
estudante = pygame.Rect(760, 180, 40, 50)

livro = pygame.Rect(470, 330, 38, 30)

# Estantes
estantes = [
    pygame.Rect(80, 80, 230, 60),
    pygame.Rect(370, 80, 230, 60),
    pygame.Rect(660, 80, 230, 60),
    pygame.Rect(80, 260, 230, 60),
    pygame.Rect(660, 260, 230, 60),
]

# Limites do cenário
limites = [
    pygame.Rect(0, 0, LARGURA, 20),
    pygame.Rect(0, ALTURA - 20, LARGURA, 20),
    pygame.Rect(0, 0, 20, ALTURA),
    pygame.Rect(LARGURA - 20, 0, 20, ALTURA),
]

# ----------------------------------------------------------
# Funções
# ----------------------------------------------------------

def texto(superficie, mensagem, x, y, fonte_usada=fonte, cor=PRETO):
    imagem = fonte_usada.render(mensagem, True, cor)
    superficie.blit(imagem, (x, y))


def texto_central(superficie, mensagem, y, fonte_usada=fonte_grande, cor=PRETO):
    imagem = fonte_usada.render(mensagem, True, cor)
    x = (LARGURA - imagem.get_width()) // 2
    superficie.blit(imagem, (x, y))


def desenhar_avatar():
    # Corpo
    pygame.draw.rect(TELA, AZUL, avatar, border_radius=7)

    # Cabeça
    pygame.draw.circle(
        TELA,
        (235, 190, 150),
        (avatar.centerx, avatar.y - 7),
        14
    )

    # Nome
    texto(TELA, nome, avatar.x - 8, avatar.y + 50, fonte_pequena)


def desenhar_personagem(rect, cor, nome_personagem):
    pygame.draw.rect(TELA, cor, rect, border_radius=8)
    pygame.draw.circle(
        TELA,
        (235, 190, 150),
        (rect.centerx, rect.y - 7),
        13
    )
    texto(TELA, nome_personagem, rect.x - 5, rect.y + 55, fonte_pequena)


def perto(a, b, distancia=75):
    return a.inflate(distancia, distancia).colliderect(b)


def adicionar_pontos(valor):
    global pontos, nivel

    pontos += valor

    if pontos >= 80:
        nivel = 4
    elif pontos >= 50:
        nivel = 3
    elif pontos >= 30:
        nivel = 2
    else:
        nivel = 1


def atualizar_recompensas():
    if pontos >= 10 and "Estudante Iniciante" not in recompensas:
        recompensas.append("Estudante Iniciante")

    if pontos >= 30 and "Leitor" not in recompensas:
        recompensas.append("Leitor")

    if pontos >= 50 and "Explorador do Conhecimento" not in recompensas:
        recompensas.append("Explorador do Conhecimento")

    if pontos >= 80 and "Mestre da Biblioteca" not in recompensas:
        recompensas.append("Mestre da Biblioteca")


def desenhar_cenario():
    TELA.fill(FUNDO)

    # Parede superior
    pygame.draw.rect(TELA, PAREDE, (20, 20, LARGURA - 40, 80))

    texto_central(
        TELA,
        "A BIBLIOTECA DO CONHECIMENTO",
        40,
        fonte_grande,
        MADEIRA
    )

    # Piso
    pygame.draw.rect(
        TELA,
        (210, 190, 160),
        (20, 100, LARGURA - 40, ALTURA - 120)
    )

    # Estantes
    for estante in estantes:
        pygame.draw.rect(TELA, MADEIRA, estante, border_radius=6)

        # Livros
        for i in range(8):
            x = estante.x + 12 + i * 27
            pygame.draw.rect(
                TELA,
                [VERMELHO, VERDE, AZUL, AMARELO, ROXO][i % 5],
                (x, estante.y + 10, 18, 42)
            )

    # Mesa central
    pygame.draw.rect(
        TELA,
        MADEIRA,
        (390, 400, 220, 55),
        border_radius=8
    )
    pygame.draw.rect(
        TELA,
        MADEIRA_CLARA,
        (410, 450, 20, 65)
    )
    pygame.draw.rect(
        TELA,
        MADEIRA_CLARA,
        (570, 450, 20, 65)
    )

    # Livro da missão
    if not livro_encontrado:
        pygame.draw.rect(TELA, VERDE, livro, border_radius=4)
        texto(TELA, "📖", livro.x + 2, livro.y - 4, fonte)
        texto(TELA, "Livro", livro.x - 2, livro.y + 35, fonte_pequena)

    # Personagens
    desenhar_personagem(professora, ROXO, "Professora")
    desenhar_personagem(estudante, VERDE, "Aluno")

    desenhar_avatar()

    # Painel lateral
    pygame.draw.rect(TELA, BRANCO, (20, 555, LARGURA - 40, 75), border_radius=8)
    pygame.draw.rect(TELA, MADEIRA, (20, 555, LARGURA - 40, 75), 2, border_radius=8)

    texto(TELA, f"Aluno: {nome}", 40, 565, fonte_pequena)
    texto(TELA, f"⭐ Pontos: {pontos}", 230, 565, fonte_pequena)
    texto(TELA, f"🏆 Nível: {nivel}", 380, 565, fonte_pequena)
    texto(TELA, f"🎁 Recompensas: {len(recompensas)}", 530, 565, fonte_pequena)

    texto(TELA, mensagem, 40, 595, fonte_pequena, MADEIRA)


def desenhar_pergunta():
    TELA.fill(FUNDO)

    pygame.draw.rect(TELA, BRANCO, (100, 70, 800, 500), border_radius=15)
    pygame.draw.rect(TELA, MADEIRA, (100, 70, 800, 500), 3, border_radius=15)

    texto_central(TELA, "DESAFIO DO CONHECIMENTO", 100, fonte_grande, MADEIRA)

    if pergunta_atual == 1:
        texto(TELA, "O que é um algoritmo?", 150, 180, fonte_grande)

        opcoes = [
            "1 - Uma sequência de passos para resolver um problema",
            "2 - Um tipo de computador",
            "3 - Um jogo eletrônico"
        ]

    else:
        texto(TELA, "Qual destes é um tipo de dado?", 150, 180, fonte_grande)

        opcoes = [
            "1 - Inteiro",
            "2 - Algoritmo",
            "3 - Computador"
        ]

    for i, opcao in enumerate(opcoes):
        y = 260 + i * 70

        if resposta_selecionada == i + 1:
            pygame.draw.rect(
                TELA,
                AMARELO,
                (140, y - 8, 720, 55),
                border_radius=8
            )

        texto(TELA, opcao, 160, y, fonte)

    texto_central(
        TELA,
        "Pressione 1, 2 ou 3 e depois ENTER",
        485,
        fonte_pequena,
        CINZA
    )


def desenhar_vitoria():
    TELA.fill(FUNDO)

    pygame.draw.rect(
        TELA,
        BRANCO,
        (120, 80, 760, 470),
        border_radius=20
    )

    pygame.draw.rect(
        TELA,
        MADEIRA,
        (120, 80, 760, 470),
        4,
        border_radius=20
    )

    texto_central(
        TELA,
        "🏆 MISSÃO CONCLUÍDA!",
        130,
        fonte_titulo,
        MADEIRA
    )

    texto_central(
        TELA,
        f"Parabéns, {nome}!",
        210,
        fonte_grande
    )

    texto_central(
        TELA,
        f"Você terminou a primeira aventura com {pontos} pontos.",
        270,
        fonte
    )

    texto_central(
        TELA,
        f"Nível alcançado: {nivel}",
        315,
        fonte
    )

    texto_central(
        TELA,
        "Recompensas conquistadas:",
        365,
        fonte
    )

    y = 405
    for recompensa in recompensas:
        texto_central(TELA, "⭐ " + recompensa, y, fonte_pequena, MADEIRA)
        y += 28

    texto_central(
        TELA,
        "Pressione ESC para sair.",
        510,
        fonte_pequena,
        CINZA
    )


# ----------------------------------------------------------
# Tela inicial
# ----------------------------------------------------------

nome_input = ""
digitando_nome = True

while digitando_nome:
    TELA.fill(FUNDO)

    texto_central(
        TELA,
        "A BIBLIOTECA DO CONHECIMENTO",
        150,
        fonte_titulo,
        MADEIRA
    )

    texto_central(
        TELA,
        "Projeto de Pensamento Computacional",
        220,
        fonte
    )

    texto_central(
        TELA,
        "Digite o nome do seu avatar:",
        300,
        fonte
    )

    pygame.draw.rect(
        TELA,
        BRANCO,
        (300, 350, 400, 55),
        border_radius=8
    )

    pygame.draw.rect(
        TELA,
        MADEIRA,
        (300, 350, 400, 55),
        2,
        border_radius=8
    )

    texto(TELA, nome_input, 320, 365, fonte)

    texto_central(
        TELA,
        "ENTER = começar",
        440,
        fonte_pequena,
        CINZA
    )

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_RETURN:
                if nome_input.strip():
                    nome = nome_input.strip()
                    digitando_nome = False

            elif evento.key == pygame.K_BACKSPACE:
                nome_input = nome_input[:-1]

            else:
                if len(nome_input) < 18 and evento.unicode.isprintable():
                    nome_input += evento.unicode

    pygame.display.flip()
    RELOGIO.tick(60)


# ----------------------------------------------------------
# Loop principal
# ----------------------------------------------------------

rodando = True

while rodando:

    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            rodando = False

        if evento.type == pygame.KEYDOWN:

            if evento.key == pygame.K_ESCAPE:
                rodando = False

            # ------------------------------------------------
            # Resposta dos desafios
            # ------------------------------------------------
            if modo == "pergunta":

                if evento.key in [pygame.K_1, pygame.K_2, pygame.K_3]:
                    resposta_selecionada = evento.key - pygame.K_0

                if evento.key == pygame.K_RETURN:

                    if resposta_selecionada is None:
                        mensagem = "Escolha uma resposta primeiro."
                    else:

                        correta = (
                            (pergunta_atual == 1 and resposta_selecionada == 1)
                            or
                            (pergunta_atual == 2 and resposta_selecionada == 1)
                        )

                        if correta:
                            if pergunta_atual not in perguntas_respondidas:
                                adicionar_pontos(10)
                                perguntas_respondidas.add(pergunta_atual)
                                atualizar_recompensas()
                                mensagem = "Resposta correta! Você ganhou 10 pontos."
                            else:
                                mensagem = "Você já respondeu este desafio."

                        else:
                            mensagem = "Resposta incorreta. Continue explorando."

                        modo = "jogo"
                        resposta_selecionada = None

            # ------------------------------------------------
            # Interação no jogo
            # ------------------------------------------------
            elif modo == "jogo":

                if evento.key == pygame.K_e:

                    if perto(avatar, professora):

                        if 1 not in perguntas_respondidas:
                            pergunta_atual = 1
                            resposta_selecionada = None
                            modo = "pergunta"
                        else:
                            mensagem = "Professora: Você já completou meu desafio!"

                    elif perto(avatar, estudante):

                        if 2 not in perguntas_respondidas:
                            pergunta_atual = 2
                            resposta_selecionada = None
                            modo = "pergunta"
                        else:
                            mensagem = "Aluno: Você já respondeu minha pergunta!"

                    elif perto(avatar, livro) and not livro_encontrado:

                        livro_encontrado = True
                        adicionar_pontos(20)
                        atualizar_recompensas()
                        mensagem = "📚 Livro encontrado! Você ganhou 20 pontos."

                    else:
                        mensagem = "Não há nada para interagir aqui."

    # ------------------------------------------------------
    # Movimento
    # ------------------------------------------------------

    if modo == "jogo":

        teclas = pygame.key.get_pressed()

        dx = 0
        dy = 0

        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            dx -= velocidade

        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            dx += velocidade

        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            dy -= velocidade

        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            dy += velocidade

        # Movimento horizontal
        avatar.x += dx

        for obstaculo in limites + estantes:
            if avatar.colliderect(obstaculo):
                if dx > 0:
                    avatar.right = obstaculo.left
                elif dx < 0:
                    avatar.left = obstaculo.right

        # Movimento vertical
        avatar.y += dy

        for obstaculo in limites + estantes:
            if avatar.colliderect(obstaculo):
                if dy > 0:
                    avatar.bottom = obstaculo.top
                elif dy < 0:
                    avatar.top = obstaculo.bottom

    # ------------------------------------------------------
    # Verificação da missão
    # ------------------------------------------------------

    if (
        livro_encontrado
        and 1 in perguntas_respondidas
        and 2 in perguntas_respondidas
        and not missao_finalizada
    ):
        missao_finalizada = True
        modo = "vitoria"
        mensagem = "Missão concluída!"

    # ------------------------------------------------------
    # Desenho
    # ------------------------------------------------------

    if modo == "jogo":
        desenhar_cenario()

    elif modo == "pergunta":
        desenhar_pergunta()

    elif modo == "vitoria":
        desenhar_vitoria()

    pygame.display.flip()
    RELOGIO.tick(60)

pygame.quit()
sys.exit()

