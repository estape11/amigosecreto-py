from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse
import random
app = Flask(__name__)

amigos = ["esteban", "susana", "fabian", "francisco", "greivin", "carmen", "mely",
          "pamela", "sofia", "grettel", "karen", "tita", "tito", "isaias", "edwin", "teresa"]
amigos_seleccionados = []
amigos_participantes = []


def obtenerAmigo(participante):
    global amigos, amigos_seleccionados
    no_encontrado = True
    amigo = ""
    intentos = 0
    while no_encontrado:
        indice_seleccionado = random.randint(0, len(amigos)-1)
        amigo = amigos[indice_seleccionado]
        if participante != amigo and not amigo in amigos_seleccionados:
            amigos_seleccionados.append(amigo)
            # print(amigos_seleccionados)
            no_encontrado = False
        intentos += 1
        if intentos > len(amigos) or len(amigos_seleccionados) == len(amigos):
            no_encontrado = False

    return amigo


@app.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    responded = False
    # Mensajes predefinidos
    if 'amigo' in incoming_msg:
        msg.body("Envía tu nombre (sin tildes ni disminutivos)")
        responded = True
    if not responded:
        participante = incoming_msg.lower()
        if not participante in amigos:
            msg.body('No estás en la lista de invitados')
        else:
            if participante in amigos_participantes:
                msg.body('Tu amigo secreto ya fue asignado')
            else:
                amigo = obtenerAmigo(participante)
                if amigo == "":
                    msg.body(
                        "Lo siento, todos los amigos ya fueron seleccionados")
                else:
                    msg.body(
                        f'Tu amigo secreto es *{amigo}* 🥳 \n El regalito es de ₡5000 \n_(🤫 no reveles esta información con nadie)_')
                    amigos_participantes.append(participante)
                    print(amigos_participantes)
    return str(resp)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
    # app.run()
