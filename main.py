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

class JogoQuiz:
    def __init__(self, root, perguntas):
        self.root = root
        self.root.title("Game School - Quiz")
        self.root.geometry("900x600")
        self.root.configure(bg="#e6f2ff")

        # Adiciona um fundo consistente em todas as telas
        self.fundo = tk.PhotoImage(file="imagens/fundo.mp3")  # Certifique-se de ter a imagem
        self.background_label = tk.Label(self.root, image=self.fundo)
        self.background_label.place(relwidth=1, relheight=1)

        self.perguntas = perguntas
        random.shuffle(self.perguntas)  # Embaralha as perguntas
        self.indice = 0
        self.pontuacao = 0

        # Configura o layout do jogo
        self.caixa = tk.Frame(self.root, bg="#ffffff", bd=5, relief="groove", width=800, height=500)
        self.caixa.place(relx=0.5, rely=0.55, anchor="center") # Ajustei a posição vertical

        # Título do Jogo
        self.titulo = tk.Label(self.caixa, text="Quiz Time!", font=("Helvetica", 28, "bold"), bg="#ffffff", fg="#007bff", pady=20) # Estilizei o título
        self.titulo.pack()

        # Configuração de exibição da pergunta
        self.label_pergunta = tk.Label(self.caixa, text="", font=("Helvetica", 18), wraplength=750, bg="#ffffff", justify="center") # Centralizei o texto
        self.label_pergunta.pack(pady=30)

        # Caixa para o jogador digitar a resposta
        self.entrada_resposta = tk.Entry(self.caixa, font=("Helvetica", 16), bd=2, relief="solid", width=50) # Aumentei a largura
        self.entrada_resposta.pack(pady=20)
        self.entrada_resposta.focus_set() # Foca na entrada ao iniciar a pergunta

        # Botão para enviar a resposta
        self.botao_enviar = tk.Button(self.caixa, text="Enviar Resposta ✅", font=("Helvetica", 16, "bold"), bg="#28a745", fg="white", command=self.verificar_resposta, padx=20, pady=10) # Estilizei o botão
        self.botao_enviar.pack(pady=20)

        # Label para mostrar o resultado da resposta
        self.label_resultado = tk.Label(self.caixa, text="", font=("Helvetica", 16), bg="#ffffff", pady=10)
        self.label_resultado.pack()

        # Exibe a primeira pergunta
        self.exibir_proxima_pergunta()

    def exibir_proxima_pergunta(self):
        if self.indice < len(self.perguntas):
            pergunta_atual = self.perguntas[self.indice]
            self.label_pergunta.config(text=pergunta_atual['pergunta'])  # Exibe a pergunta
            self.entrada_resposta.delete(0, tk.END)  # Limpa a caixa de resposta
            self.label_resultado.config(text="")  # Limpa o resultado da resposta anterior
            self.entrada_resposta.focus_set() # Refoca na entrada ao exibir nova pergunta
        else:
            self.mostrar_resultado_final()  # Se todas as perguntas foram feitas, mostra o resultado final

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

        self.indice += 1  # Passa para a próxima pergunta
        self.root.after(1500, self.exibir_proxima_pergunta)  # Reduzi o tempo de espera

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

        pygame.mixer.Sound("sons/final.mp3").play()
        tk.Label(self.caixa, text=mensagem, font=("Helvetica", 20, "bold"), wraplength=750, bg="#ffffff", justify="center").pack(pady=40)

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

        # Aqui você pode salvar as perguntas no seu "banco de dados" (por exemplo, um arquivo JSON)
        # Por enquanto, vamos apenas iniciar o jogo diretamente.
        iniciar_jogo(perguntas)

    except Exception as e:
        messagebox.showerror("Erro ao importar", str(e))

# Função para escolher o tipo de jogo
def escolher_tipo_jogo():
    escolha_janela = tk.Toplevel(root)
    escolha_janela.title("Escolher Tipo de Jogo")
    escolha_janela.geometry("400x200")
    escolha_janela.configure(bg="#e6f2ff")

    label