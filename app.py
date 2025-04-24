from flask import Flask, render_template, request
import boto3
import openai
import os
from dotenv import load_dotenv
import uuid

load_dotenv()

app = Flask(__name__)
app.secret_key = "llaveultrasecreta"

# Configurar acceso a DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('uip_recomendacion')

# Cliente de OpenAI con API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/enviar_informacion/", methods=["POST"])
def enviar_informacion():
    try:
        id_promp = str(uuid.uuid4()) 
        intereses = request.form.get("intereses")
        habilidades = request.form.get("habilidades")
        metas = request.form.get("metas")

        prompt = f"""
        Soy un orientador académico de la Universidad Interamericana de Panamá. 
        El usuario tiene los siguientes intereses: {intereses}, habilidades: {habilidades}, y metas: {metas}.
        ¿Qué carrera universitaria le recomiendas estudiar?
        """

        # Cambio a la nueva API de OpenAI
        respuesta = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "Eres un orientador académico."},
                      {"role": "user", "content": prompt}],
            max_tokens=200
        )
        
        # Obtención de la respuesta
        recomendacion = respuesta['choices'][0]['message']['content']

        # Guardar en DynamoDB
        table.put_item(
            Item={
                'id_promp': id_promp,
                'intereses': intereses,
                'habilidades': habilidades,
                'metas': metas,
                'prompt': prompt,
                'recomendacion': recomendacion
            }
        )

        return render_template("index.html", recomendacion=recomendacion)

    except Exception as e:
        return f"Ocurrió un error: {e}"

if __name__ == "__main__":
    app.run(debug=True)
