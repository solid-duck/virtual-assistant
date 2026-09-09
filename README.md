# GrooveStreet Records - Assistente Virtuale 🎸

Assistente virtuale interattivo per il negozio di dischi **GrooveStreet Records**, realizzato con **Chainlit**, la **Responses API di OpenAI** e **Resend** per l'invio delle email automatiche.

---

## 🛠️ Requisiti e Installazione

1. Assicurati di avere **Python 3.10** o superiore installato sul tuo computer.
2. Clona o apri la cartella del progetto nel tuo terminale.
3. Installa le dipendenze richieste tramite `pip`:
   ```bash
   pip install -r requirements.txt

# Per avviare l'assistente virtuale, esegui il seguente comando:
    ``` poetry run chainlit run virtual-assistant/app.py -w

Esempi di Domande da Fare all'Assistente (Prompt di Test)
Ecco alcuni esempi di test da fare per verificare il corretto funzionamento del catalogo e della funzione di invio email:

Informazioni sul negozio e orari:

"Ciao! Quali sono i vostri orari di apertura?"

"Dove si trova esattamente il negozio?"

Ricerca dischi e prezzi:

"Avete in catalogo l'album di Miles Davis?"

"Quanto costa la versione in vinile dei Pink Floyd?"

"Mi consigli qualche disco rock o jazz?"

Invio email automatica (Funzione personalizzata):

"Vorrei ricevere il catalogo aggiornato via email, mi chiamo Mario Rossi e la mia email è mario.rossi@email.com"