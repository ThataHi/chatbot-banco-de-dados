import re

class MetaAI:
    def prompt(self, message):
        message_lower = message.lower()

        # Resposta simpática
        if any(saud in message_lower for saud in ["bom dia", "boa tarde", "boa noite", "olá", "oi"]):
            return {"message": "Olá! Como posso ajudar você com informações do IFSP Campinas?"}

        # Consulta por curso
        if "curso" in message_lower:
            return {"message": "SELECT DISTINCT curso FROM dados_ifsp;"}

        # Consulta por disciplina com filtro por professor
        if "disciplina" in message_lower or "aula" in message_lower or "matéria" in message_lower:
            prof_match = re.search(r"professor[a]? (\w+)", message_lower)
            if prof_match:
                nome_prof = prof_match.group(1).capitalize()
                return {"message": f"SELECT DISTINCT disciplina FROM dados_ifsp WHERE professor LIKE '%{nome_prof}%';"}

            sala_match = re.search(r"sala (\w+)", message_lower)
            if sala_match:
                sala = sala_match.group(1).upper()
                return {"message": f"SELECT DISTINCT disciplina FROM dados_ifsp WHERE sala LIKE '%{sala}%';"}

            return {"message": "SELECT DISTINCT disciplina FROM dados_ifsp;"}

        # Consulta por sala
        if "sala" in message_lower:
            return {"message": "SELECT DISTINCT sala FROM dados_ifsp;"}

        # Consulta por professor
        if "professor" in message_lower:
            return {"message": "SELECT DISTINCT professor FROM dados_ifsp;"}

        # Consulta por horário
        if "horário" in message_lower or "horario" in message_lower:
            return {"message": "SELECT DISTINCT horario FROM dados_ifsp;"}

        return {"message": "FORA DO ESCOPO"}
