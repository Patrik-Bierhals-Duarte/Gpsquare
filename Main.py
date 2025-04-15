import tkinter as tk


TAMANHO = 5
TAMANHO_CELULA = 60


COR_FUNDO = "#2B2B2B"
COR_LINHA = "#FFFFFF"
COR_OBSTACULO = "#CC0000"
COR_CAMINHO = "#00CC00"
COR_INICIO = "#0066FF"
COR_DESTINO = "#FFD700"


proximo_passo = False


def criar_tabuleiro():
    tabuleiro = [[" " for _ in range(TAMANHO)] for _ in range(TAMANHO)]


    obstaculos = [
        (2, 1), (4, 1), (2, 3),
        (1, 2), (4, 4), (1, 4),(0, 0)
    ]

    for (linha, coluna) in obstaculos:
        tabuleiro[linha][coluna] = "X"

    return tabuleiro



def desenhar_tabuleiro(canvas, tabuleiro, caminho, posicao_inicial, destino):
    canvas.delete("all")

    for i in range(TAMANHO):
        for j in range(TAMANHO):
            cor = COR_FUNDO
            if tabuleiro[i][j] == "X":
                cor = COR_OBSTACULO
            elif (i, j) == posicao_inicial:
                cor = COR_INICIO
            elif (i, j) == destino:
                cor = COR_DESTINO
            elif (i, j) in caminho:
                cor = COR_CAMINHO

            canvas.create_rectangle(
                j * TAMANHO_CELULA, i * TAMANHO_CELULA,
                (j + 1) * TAMANHO_CELULA, (i + 1) * TAMANHO_CELULA,
                fill=cor, outline=COR_LINHA
            )

    canvas.update()



def movimento_valido(tabuleiro, linha, coluna):
    return 0 <= linha < TAMANHO and 0 <= coluna < TAMANHO and tabuleiro[linha][coluna] == " "


def encontrar_caminho(canvas, tabuleiro, linha_atual, coluna_atual, destino, caminho):
    global proximo_passo

    if (linha_atual, coluna_atual) == destino:
        exibir_tela_final(canvas)  # Chama tela final ao chegar ao destino
        return True

    direcoes = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    for direcao in direcoes:
        nova_linha = linha_atual + direcao[0]
        nova_coluna = coluna_atual + direcao[1]

        if movimento_valido(tabuleiro, nova_linha, nova_coluna):
            tabuleiro[nova_linha][nova_coluna] = "*"
            caminho.append((nova_linha, nova_coluna))

            desenhar_tabuleiro(canvas, tabuleiro, caminho, posicao_inicial, destino)

            proximo_passo = False
            while not proximo_passo:
                canvas.update()

            if encontrar_caminho(canvas, tabuleiro, nova_linha, nova_coluna, destino, caminho):
                return True

            caminho.pop()
            tabuleiro[nova_linha][nova_coluna] = " "

    return False



def avancar_passo(event):
    global proximo_passo
    proximo_passo = True



def exibir_tela_final(canvas):
    canvas.delete("all")
    canvas.create_text(
        TAMANHO_CELULA * TAMANHO // 2, TAMANHO_CELULA * TAMANHO // 2,
        text="🎉 CHEGOU AO DESTINO! 🎉",
        font=("Arial", 15, "bold"), fill="white"
    )
    canvas.update()



def exibir_menu_inicial(root, canvas):
    canvas.delete("all")

    texto_rgb = canvas.create_text(
        TAMANHO_CELULA * TAMANHO // 2, TAMANHO_CELULA * TAMANHO // 2,
        text="Clique ENTER para começar\nENTER para andar",
        font=("Arial", 15, "bold"), fill="red"
    )


    def animar_texto():
        cores = ["red", "green", "blue", "yellow", "purple", "white"]
        for cor in cores:
            canvas.itemconfig(texto_rgb, fill=cor)
            root.update()
            root.after(300)

    root.after(100, animar_texto)
    root.bind("<Return>", lambda event: iniciar_jogo(root, canvas))



def iniciar_jogo(root, canvas):
    tabuleiro = criar_tabuleiro()

    global posicao_inicial, destino
    posicao_inicial = (4, 0)
    destino = (0, 4)
    caminho = [posicao_inicial]

    root.bind("<Return>", avancar_passo)

    desenhar_tabuleiro(canvas, tabuleiro, caminho, posicao_inicial, destino)

    root.after(500,
               lambda: encontrar_caminho(canvas, tabuleiro, posicao_inicial[0], posicao_inicial[1], destino, caminho))


def main():
    root = tk.Tk()
    root.title("Backtracking Visual")
    root.configure(bg=COR_FUNDO)

    canvas = tk.Canvas(root, width=TAMANHO * TAMANHO_CELULA, height=TAMANHO * TAMANHO_CELULA, bg=COR_FUNDO)
    canvas.pack()

    exibir_menu_inicial(root, canvas)

    root.mainloop()


main()