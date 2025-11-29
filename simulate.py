import random

def simular_entrada_saida(tempo_total, probabilidade_interrupcao):
    """
    Simula o processamento com interrupções de E/S.
    
    Args:
        tempo_total (int): Duração da simulação em ciclos de clock.
        probabilidade_interrupcao (int): Chance (0-100) de gerar uma interrupção a cada ciclo.
    """
    
    # Definição dos Dispositivos e Prioridades
    # Prioridade: 3 (Alta), 2 (Média), 1 (Baixa)
    dispositivos = [
        {"nome": "Teclado", "prioridade": 3, "tipo": "Alta", "tempo_tratamento": 2},
        {"nome": "Impressora", "prioridade": 2, "tipo": "Média", "tempo_tratamento": 4},
        {"nome": "Disco", "prioridade": 1, "tipo": "Baixa", "tempo_tratamento": 5}
    ]

    # Contexto do Processo Principal (simulado por um contador de instruções)
    contexto_processo = 0
    
    # Logs para o frontend
    log_eventos = []
    
    relogio = 0
    
    log_eventos.append({
        "tempo": relogio,
        "tipo": "INFO",
        "mensagem": "Início da simulação. Processo Principal carregado.",
        "contexto": contexto_processo
    })

    while relogio < tempo_total:
        
        # 1. Verificar se ocorrem interrupções neste ciclo
        interrupcoes_neste_ciclo = []
        
        # Simula a chegada aleatória (pode haver múltiplas ao mesmo tempo)
        if random.randint(1, 100) <= probabilidade_interrupcao:
            # Escolhe um dispositivo aleatório que gerou a interrupção
            dev = random.choice(dispositivos)
            interrupcoes_neste_ciclo.append(dev)
            
            # Chance pequena de uma segunda interrupção simultânea (para testar prioridade)
            if random.randint(1, 100) <= 30:
                dev2 = random.choice(dispositivos)
                interrupcoes_neste_ciclo.append(dev2)

        # 2. Se houver interrupções, o SO precisa agir
        if interrupcoes_neste_ciclo:
            
            # ORDENAR POR PRIORIDADE (Maior prioridade primeiro)
            # Isso cumpre o requisito de tratar conforme a prioridade
            interrupcoes_neste_ciclo.sort(key=lambda x: x["prioridade"], reverse=True)
            
            # Para cada interrupção na fila (da maior para menor prioridade)
            for dispositivo in interrupcoes_neste_ciclo:
                
                # A. Salvar Contexto
                log_eventos.append({
                    "tempo": relogio,
                    "tipo": "INTERRUPCAO",
                    "dispositivo": dispositivo["nome"],
                    "prioridade_desc": dispositivo["tipo"],
                    "mensagem": f"Interrupção recebida ({dispositivo['nome']}). Salvando contexto (PC={contexto_processo})...",
                    "contexto": contexto_processo
                })
                
                contexto_salvo = contexto_processo # "Salva" na memória (variável)
                
                # B. Tratar a Interrupção (O tempo avança durante o tratamento)
                tempo_tratamento = dispositivo["tempo_tratamento"]
                log_eventos.append({
                    "tempo": relogio + 1,
                    "tipo": "TRATAMENTO",
                    "mensagem": f"Tratando requisição do {dispositivo['nome']} (Duração: {tempo_tratamento} ciclos)...",
                    "contexto": "Sistema Operacional"
                })
                
                relogio += tempo_tratamento
                
                # C. Restaurar Contexto
                contexto_processo = contexto_salvo # "Restaura" da memória
                
                log_eventos.append({
                    "tempo": relogio,
                    "tipo": "RETORNO",
                    "mensagem": f"Interrupção finalizada. Restaurando contexto (PC={contexto_processo}). Retomando processo.",
                    "contexto": contexto_processo
                })

        else:
            # 3. Se não houver interrupção, o Processo Principal executa
            contexto_processo += 1 # Simula processar uma instrução
            
            # Loga apenas periodicamente para não poluir demais, ou se for solicitado
            # Vamos logar execução normal apenas para visualização
            log_eventos.append({
                "tempo": relogio,
                "tipo": "EXECUCAO",
                "mensagem": "Processo Principal em execução (CPU Ocupada).",
                "contexto": contexto_processo
            })
            
            relogio += 1

    log_eventos.append({
        "tempo": relogio,
        "tipo": "FIM",
        "mensagem": "Tempo limite atingido. Simulação encerrada.",
        "contexto": contexto_processo
    })

    return {
        "log": log_eventos,
        "total_ciclos": relogio,
        "instrucoes_executadas": contexto_processo
    }