from flask import Flask, render_template, redirect, request, flash
import requests
import os

ENDPOINT_API = "https://api.thecatapi.com/v1/images/search"

app = Flask(__name__)
app.secret_key = "Sociedade Secreta dos Gatinhos"

# Criar pasta de Download caso não exista
UPLOAD_FOLDER = "static/downloads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# Rota da Página Inicial
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


# Rota para processar a solicitação
@app.route("/newcat", methods=["GET", "POST"])
def kitten():
    if request.method == "GET":
        return redirect("/")

    nome = request.form.get("nome", None)

    if not nome:
        erro = "ERRO! Você precisa digitar um nome"
        return redirect("/")

    resposta = requests.get(ENDPOINT_API)

    if resposta.status_code == 200:
        dados = resposta.json()  # JSON para DIC
        url_image = dados[0]["url"]

        # Desafio: Pegar a foto + nome e salvar
        try:
            extensao = url_image.split(".")[-1]
            nome_arquivo = f"{nome}_{dados[0]['id']}.{extensao}"  # Nome + id para evitar duplicação
            caminho_completo = os.path.join(UPLOAD_FOLDER, nome_arquivo)

            # download da imagem
            img_data = requests.get(url_image).content
            with open(caminho_completo, "wb") as handler:
                handler.write(img_data)

            # Caminho para o HTML mostrar a imagem local
            url_local = f"downloads/{nome_arquivo}"

        except Exception:
            flash(f"Erro ao salvar imagem: {e}")
            return redirect("/")

    else:
        flash("ERRO! Os gatos estão dormindo. Volte mais tarde.")
        return redirect("/")

    return render_template("index.html", nome=nome, url_image=url_local, salvo=True)


if __name__ == "__main__":
    app.run(debug=True)
