from dataclasses import dataclass
from typing import Optional
import json
import resend
from openai import OpenAI

@dataclass
class Message:
    role: str
    content: str

class ChatLogic:
    def __init__(self, openai_key: str, resend_key: str):
        self.client = OpenAI(api_key=openai_key)
        resend.api_key = resend_key
        self.last_response_id = None

    def send_email(self, name: str, email: str) -> str:
        try:
            resend.Emails.send({
                "from": "onboarding@resend.dev",
                "to": email,
                "subject": "Benvenuto da GrooveStreet Records! Ecco il tuo catalogo",
                "html": f"""
                    <p>Ciao {name},<br/>
                    Grazie per aver visitato GrooveStreet Records! In allegato trovi il link al nostro catalogo vinili aggiornato.<br/>
                    </p>
                    Rock on! <br/>
                    GrooveStreet Records
                """
            })
            return "Email sent successfully"
        except Exception as e:
            return f"Failed to send email: {str(e)}"

    def process_message(self, user_message: str) -> Optional[str]:
        tools = [
            {
                "type": "function",
                "name": "send_email",
                "description": "Invia un'email al cliente quando fornisce il proprio nome e indirizzo email",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "nome del cliente"},
                        "email": {"type": "string", "description": "email del cliente"}
                    },
                    "required": ["name", "email"]
                }
            }
        ]

        payload = {
            "model": "gpt-4o-mini",
            "input": user_message,
            "instructions": "Sei Leo, l'assistente di GrooveStreet Records, un negozio di dischi in vinile. Aiuta i clienti e, se ti forniscono nome ed email, usa la funzione send_email.",
            "tools": tools
        }

        if self.last_response_id:
            payload["previous_response_id"] = self.last_response_id

        response = self.client.responses.create(**payload)
        self.last_response_id = response.id

        if response.output and any(item.type == "function_call" for item in response.output):
            for item in response.output:
                if item.type == "function_call":
                    fn_name = item.name
                    fn_args = json.loads(item.arguments)
                    call_id = item.call_id

                    if fn_name == "send_email":
                        output_result = self.send_email(**fn_args)
                    else:
                        output_result = f"Funzione sconosciuta: {fn_name}"

                    follow_up = self.client.responses.create(
                        model="gpt-4o-mini",
                        input=[{
                            "type": "function_call_output",
                            "call_id": call_id,
                            "output": output_result
                        }],
                        previous_response_id=self.last_response_id,
                        instructions="Sei Leo di GrooveStreet Records. Conferma al cliente che l'email è stata inviata con successo."
                    )
                    self.last_response_id = follow_up.id
                    
                    for out_item in follow_up.output:
                        if hasattr(out_item, "content") and out_item.content:
                            return out_item.content[0].text

        for item in response.output:
            if hasattr(item, "content") and item.content:
                return item.content[0].text

        return "Scusa, non ho capito bene la richiesta."