import random
import tkinter as tk
from tkinter import filedialog, messagebox
import pygame
import os
from docx import Document
import fitz  # PyMuPDF

# Inicializa o pygame e o mixer
pygame.init()
pygame.mixer.init()

# Cores personalizadas - Sóbrias
cor_principal = "#333333"  # Cinza escuro
cor_secundaria = "#555555"  # Cinza um pouco mais claro
cor_texto_principal = "#ffffff"
cor_fundo = "#f0f0f0"      # Cinza claro elegante
cor_caixa_texto = "#ffffff" # Branco para a caixa de texto

# Estilos de fonte - Clássicos
fonte_titulo = ("Times New Roman", 32, "bold")
fonte_botao = ("Times New Roman", 18, "bold")
fonte_texto = ("Times New Roman", 16)

class JogoQuiz:
    def __init__(self, root, perguntas):
        self.root = root
        self.root.title("Game School - Quiz")
        self.root.geometry("900x600")
        self.root.configure(bg=cor_fundo)

        # Background de cor sólida
        self.background_label = tk.Label(self.root, bg=cor_fundo)
        self.background_label.place(relwidth=1, relheight=1)

        self.perguntas = perguntas
        random.shuffle(self.perguntas)
        self.indice = 0
        self.pontuacao = 0

        # Configura o layout do jogo - Mais clássico
        self.caixa = tk.Frame(self.root, bg=cor_caixa_texto, bd=5, relief="groove", width=700, height=450)
        self.caixa.place(relx=0.5, rely=0.55, anchor="center")

        # Título do Jogo
        self.titulo = tk.Label(self.caixa, text="Quiz Time!", font=fonte_titulo, bg=cor_caixa_texto, fg=cor_principal, pady=30)
        self.titulo.pack()

        # Configuração de exibição da pergunta
        self.label_pergunta = tk.Label(self.caixa, text="", font=fonte_texto, wraplength=650, bg=cor_caixa_texto, justify="center", pady=20)
        self.label_pergunta.pack()

        # Caixa para o jogador digitar a resposta - Cantos arredondados (simulado com borda)
        self.entrada_resposta = tk.Entry(self.caixa, font=fonte_texto, bd=8, relief="solid", width=50, highlightthickness=2, highlightbackground=cor_principal)
        self.entrada_resposta.pack(pady=20)
        self.entrada_resposta.focus_set()

        # Botão para enviar a resposta
        self.botao_enviar = tk.Button(self.caixa, text="Enviar Resposta ✅", font=fonte_botao, bg=cor_secundaria, fg=cor_texto_principal, command=self.verificar_resposta, padx=30, pady=15, relief="raised", borderwidth=3)
        self.botao_enviar.pack(pady=30)

        # Label para mostrar o resultado da resposta
        self.label_resultado = tk.Label(self.caixa, text="", font=fonte_texto, bg=cor_caixa_texto, pady=15)
        self.label_resultado.pack()

        # Exibe a primeira pergunta
        self.exibir_proxima_pergunta()

    def exibir_proxima_pergunta(self):
        if self.indice < len(self.perguntas):
            pergunta_atual = self.perguntas[self.indice]
            self.label_pergunta.config(text=pergunta_atual['pergunta'])
            self.entrada_resposta.delete(0, tk.END)
            self.label_resultado.config(text="")
            self.entrada_resposta.focus_set()
        else:
            self.mostrar_resultado_final()

    def verificar_resposta(self):
        resposta = self.entrada_resposta.get().strip().lower()
        resposta_correta = self.perguntas[self.indice]['resposta'].strip().lower()

        if resposta == resposta_correta:
            self.pontuacao += 1
            self.label_resultado.config(text="✔️ Correto!", fg="green")
            try:
                pygame.mixer.Sound("sons/acerto.mp3").play()
            except pygame.error as e:
                print(f"Erro ao reproduzir som de acerto: {e}")
        else:
            self.label_resultado.config(text=f"❌ Errado! Resposta correta: {resposta_correta}", fg="red")
            try:
                pygame.mixer.Sound("sons/erro.mp3").play()
            except pygame.error as e:
                print(f"Erro ao reproduzir som de erro: {e}")

        self.indice += 1
        self.root.after(1500, self.exibir_proxima_pergunta)

    def mostrar_resultado_final(self):
        for widget in self.caixa.winfo_children():
            widget.destroy()

        total = len(self.perguntas)
        porcentagem = (self.pontuacao / total) * 100
        mensagem = f"Resultado Final:\nVocê acertou {self.pontuacao} de {total} perguntas ({porcentagem:.2f}%).\n\n"

        if porcentagem == 100:
            mensagem += "🎉 INCRÍVEL! Você é um mestre! 🏆🥇📚"
        elif porcentagem >= 80:
            mensagem += "🥳 Excelente trabalho! Continue aprendendo!"
        elif porcentagem >= 60:
            mensagem += "👏 Muito bom! Mais um esforço e você dominará tudo!"
        else:
            mensagem += "💡 Não desanime! A prática leva à perfeição. Tente novamente! 💪"

        try:
            pygame.mixer.Sound("sons/final.mp3").play()
        except pygame.error as e:
            print(f"Erro ao reproduzir som final: {e}")
        tk.Label(self.caixa, text=mensagem, font=("Times New Roman", 24, "bold"), wraplength=650, bg=cor_caixa_texto, justify="center").pack(pady=40)

# Função para importar as perguntas dos arquivos
def importar_perguntas(tipo_jogo):
    arquivo = filedialog.askopenfilename(filetypes=[("Arquivos de texto", "*.txt"),
                                                   ("Documentos Word", "*.docx"),
                                                   ("PDFs", "*.pdf")])

    if not arquivo:
        return

    ext = os.path.splitext(arquivo)[-1].lower()
    perguntas = []

    try:
        linhas = []
        if ext == ".txt":
            with open(arquivo, "r", encoding="utf-8") as f:
                linhas = f.readlines()
        elif ext == ".docx":
            doc = Document(arquivo)
            linhas = [p.text for p in doc.paragraphs]
        elif ext == ".pdf":
            doc = fitz.open(arquivo)
            for page in doc:
                linhas.extend(page.get_text().splitlines())
        else:
            messagebox.showerror("Erro", "Formato de arquivo não suportado.")
            return

        pergunta = ""
        resposta = ""

        for linha in linhas:
            linha = linha.strip()
            if linha.lower().startswith("pergunta:"):
                pergunta = linha[len("pergunta:"):].strip()
            elif linha.lower().startswith("resposta:"):
                resposta = linha[len("resposta:"):].strip()
                if pergunta and resposta:
                    perguntas.append({"pergunta": pergunta, "resposta": resposta})
                    pergunta = ""
                    resposta = ""

        if not perguntas:
            raise ValueError("Nenhuma pergunta válida encontrada.")

        iniciar_jogo(perguntas)

    except Exception as e:
        messagebox.showerror("Erro ao importar", str(e))

# Função para escolher o tipo de jogo
def escolher_tipo_jogo():
    escolha_janela = tk.Toplevel(root)
    escolha_janela.title("Escolher Tipo de Jogo")
    escolha_janela.geometry("400x200")
    escolha_janela.configure(bg=cor_fundo)

    label_escolha = tk.Label(escolha_janela, text="Escolha o tipo de jogo:", font=fonte_texto, bg=cor_fundo, fg=cor_principal, pady=20)
    label_escolha.pack()

    btn_quiz = tk.Button(escolha_janela, text="Quiz", font=fonte_botao, bg=cor_secundaria, fg=cor_texto_principal, relief="raised", padx=30, pady=15, command=lambda: importar_perguntas("quiz"))
    btn_quiz.pack(pady=10)

    btn_palavras_cruzadas = tk.Button(escolha_janela, text="Palavras Cruzadas (Em breve)", font=fonte_botao, bg="#cccccc", fg="gray", relief="raised", state="disabled", padx=30, pady=15)
    btn_palavras_cruzadas.pack(pady=10)

# Configuração inicial da interface com o Tkinter
root = tk.Tk()
root.title("Game School - Menu")
root.geometry("900x600")
root.configure(bg=cor_fundo)

# Background de cor sólida na tela inicial
background_label_menu = tk.Label(root, bg=cor_fundo)
background_label_menu.place(relwidth=1, relheight=1)

frame_menu = tk.Frame(root, bg=cor_fundo, bd=5, relief="groove", width=400, height=300)
frame_menu.place(relx=0.5, rely=0.5, anchor="center")

# Título da tela inicial
titulo_inicial = tk.Label(frame_menu, text="Game School!", font=fonte_titulo, bg=cor_fundo, fg=cor_principal, pady=40)
titulo_inicial.pack()

# Botões da tela inicial
btn_jogar = tk.Button(frame_menu, text="Jogar 🎮", font=fonte_botao, bg=cor_secundaria, fg=cor_texto_principal, relief="raised", command=escolher_tipo_jogo, padx=40, pady=20)
btn_jogar.pack(pady=20)

btn_importar = tk.Button(frame_menu, text="Importar Perguntas 📂", font=fonte_botao, bg=cor_principal, fg=cor_texto_secundaria, relief="raised", command=lambda: importar_perguntas(None), padx=40, pady=20)
btn_importar.pack(pady=20)

root.mainloop()