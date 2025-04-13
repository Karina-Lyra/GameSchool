import tkinter as tk
import pygame
import random

pygame.init()
pygame.mixer.init()

class JogoQuiz:
    def __init__(self, root, perguntas, voltar_callback):
        self.root = root
        self.root.title("Game School - Quiz")
        self.root.geometry("900x600")
        self.root.configure(bg="#001f33")

        self.perguntas = perguntas
        random.shuffle(self.perguntas)
        self.indice = 0
        self.pontuacao = 0
        self.voltar_callback = voltar_callback

        self.fundo = tk.PhotoImage(file="imagens/fundo.png")
        self.background_label = tk.Label(self.root, image=self.fundo)
        self.background_label.place(relwidth=1, relheight=1)

        self.caixa = tk.Frame(self.root, bg="#ffffff", bd=5, relief="ridge", width=800, height=500)
        self.caixa.place(relx=0.5, rely=0.5, anchor="center")

        self.label_pergunta = tk.Label(self.caixa, text="", font=("Inter", 16), wraplength=750, bg="#ffffff")
        self.label_pergunta.pack(pady=20)

        self.entrada_resposta = tk.Entry(self.caixa, font=("Inter", 14))
        self.entrada_resposta.pack()

        self.botao_enviar = tk.Button(self.caixa, text="Responder ✅", font=("Inter", 14), bg="#007acc", fg="white", command=self.verificar_resposta)
        self.botao_enviar.pack(pady=10)

        self.label_resultado = tk.Label(self.caixa, text="", font=("Inter", 14), bg="#ffffff")
        self.label_resultado.pack()

        self.exibir_proxima_pergunta()

    def exibir_proxima_pergunta(self):
        if self.indice < len(self.perguntas):
            pergunta_atual = self.perguntas[self.indice]
            self.label_pergunta.config(text=pergunta_atual['pergunta'])
            self.entrada_resposta.delete(0, tk.END)
            self.label_resultado.config(text="")
        else:
            self.mostrar_resultado_final()

    def verificar_resposta(self):
        resposta = self.entrada_resposta.get().strip().lower()
        resposta_correta = self.perguntas[self.indice]['resposta'].strip().lower()

        if resposta == resposta_correta:
            self.pontuacao += 1
            self.label_resultado.config(text="✔️ Correto!", fg="green")
            pygame.mixer.Sound("sons/acerto.mp3").play()
        else:
            self.label_resultado.config(text=f"❌ Errado! Resposta correta: {resposta_correta}", fg="red")
            pygame.mixer.Sound("sons/erro.mp3").play()

        self.indice += 1
        self.root.after(2000, self.exibir_proxima_pergunta)

    def mostrar_resultado_final(self):
        for widget in self.caixa.winfo_children():
            widget.destroy()

        total = len(self.perguntas)
        porcentagem = (self.pontuacao / total) * 100
        mensagem = f"Você acertou {self.pontuacao} de {total} perguntas.\n\n"

        if porcentagem == 100:
            mensagem += "🎉 INCRÍVEL! Você acertou tudo! Parabéns, gênio do conhecimento! 🏆"
        elif porcentagem >= 80:
            mensagem += "🥳 Excelente resultado! Continue assim!"
        elif porcentagem >= 60:
            mensagem += "👏 Parabéns! Está indo bem, mas sempre dá pra melhorar!"
        else:
            mensagem += "💡 Não desista! Estude mais e tente novamente!"

        pygame.mixer.Sound("sons/final.mp3").play()
        tk.Label(self.caixa, text=mensagem, font=("Inter", 16), wraplength=750, bg="#ffffff").pack(pady=20)

        tk.Button(self.caixa, text="🔙 Voltar ao Menu", font=("Inter", 14), bg="#007acc", fg="white", command=self.voltar_callback).pack(pady=20)
