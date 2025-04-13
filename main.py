import tkinter as tk
from tkinter import filedialog, messagebox
import os
import docx
import PyPDF2
import json

# Função para extrair perguntas e respostas do texto
def extrair_perguntas_respostas(texto):
    blocos = texto.strip().split("Pergunta:")
    perguntas_respostas = []

    for bloco in blocos:
        if "Resposta:" in bloco:
            partes = bloco.strip().split("Resposta:")
            pergunta = partes[0].strip()
            resposta = partes[1].strip()
            perguntas_respostas.append({"pergunta": pergunta, "resposta": resposta})

    return perguntas_respostas

# Função para ler arquivos
def ler_arquivo(caminho):
    ext = os.path.splitext(caminho)[1].lower()

    if ext == ".txt":
        with open(caminho, "r", encoding="utf-8") as f:
            return f.read()

    elif ext == ".pdf":
        texto = ""
        with open(caminho, "rb") as f:
            leitor = PyPDF2.PdfReader(f)
            for pagina in leitor.pages:
                texto += pagina.extract_text()
        return texto

    elif ext == ".docx":
        doc = docx.Document(caminho)
        return "\n".join([p.text for p in doc.paragraphs])

    else:
        raise ValueError("Formato não suportado.")

# Função chamada ao clicar no botão
def importar_arquivo():
    caminho = filedialog.askopenfilename(filetypes=[("Arquivos de texto", "*.txt *.pdf *.docx")])
    if not caminho:
        return

    try:
        texto = ler_arquivo(caminho)
        perguntas_respostas = extrair_perguntas_respostas(texto)

        if not perguntas_respostas:
            messagebox.showwarning("Aviso", "Nenhuma pergunta encontrada no arquivo.")
            return

        # Salva num arquivo json (pode ser SQLite depois)
        with open("perguntas.json", "w", encoding="utf-8") as f:
            json.dump(perguntas_respostas, f, ensure_ascii=False, indent=2)

        messagebox.showinfo("Sucesso", f"{len(perguntas_respostas)} perguntas importadas com sucesso!")

    except Exception as e:
        messagebox.showerror("Erro", str(e))

# Criação da janela principal
janela = tk.Tk()
janela.title("Importador de Perguntas")
janela.geometry("400x200")

label = tk.Label(janela, text="Importar perguntas e respostas", font=("Arial", 14))
label.pack(pady=20)

botao = tk.Button(janela, text="Selecionar Arquivo", command=importar_arquivo, bg="blue", fg="white", font=("Arial", 12))
botao.pack(pady=10)

janela.mainloop()

