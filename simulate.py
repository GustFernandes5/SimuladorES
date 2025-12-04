import random

def simular_entrada_saida(tempo_total, probabilidade_interrupcao):
    """
    Simula o processamento com interrupções de E/S e salva log em TXT.
    """
    
    # Definição dos Dispositivos e Prioridades
    dispositivos = [
        {"nome": "Teclado", "prioridade": 3, "tipo": "Alta", "tempo_tratamento": 2},
        {"nome": "Impressora", "prioridade": 2, "tipo": "Média", "tempo_tratamento": 4},
        {"nome": "Disco", "prioridade": 1, "tipo": "Baixa", "tempo_tratamento": 5}
    ]

    contexto_processo = 0
    log_eventos = []
    relogio = 0
    
    # Evento inicial
    log_eventos.append({
        "tempo": relogio,
        "tipo": "INFO",
        "mensagem": "Início da simulação. Processo Principal carregado.",
        "contexto": contexto_processo
    })

    while relogio < tempo_total:
        
        # 1. Verificar se ocorrem interrupções neste ciclo
        interrupcoes_neste_ciclo = []
        
        if random.randint(1, 100) <= probabilidade_interrupcao:
            dev = random.choice(dispositivos)
            interrupcoes_neste_ciclo.append(dev)
            
            # Chance de segunda interrupção (teste de prioridade na mesma unidade de tempo)
            if random.randint(1, 100) <= 30:
                dev2 = random.choice(dispositivos)
                interrupcoes_neste_ciclo.append(dev2)

        # 2. Se houver interrupções, o SO precisa agir
        if interrupcoes_neste_ciclo:
            
            # ORDENAR POR PRIORIDADE (Requisito fundamental)
            interrupcoes_neste_ciclo.sort(key=lambda x: x["prioridade"], reverse=True)
            
            for dispositivo in interrupcoes_neste_ciclo:
                
                # A. Salvar Contexto
                log_eventos.append({
                    "tempo": relogio,
                    "tipo": "INTERRUPCAO",
                    "mensagem": f"Interrupção recebida ({dispositivo['nome']} - Prio: {dispositivo['tipo']}). Salvando contexto...",
                    "contexto": contexto_processo
                })
                
                contexto_salvo = contexto_processo 
                
                # B. Tratar a Interrupção
                tempo_tratamento = dispositivo["tempo_tratamento"]
                log_eventos.append({
                    "tempo": relogio + 1,
                    "tipo": "TRATAMENTO",
                    "mensagem": f"Tratando requisição do {dispositivo['nome']} (Duração: {tempo_tratamento} ciclos)...",
                    "contexto": "Sistema Operacional"
                })
                
                relogio += tempo_tratamento
                
                # C. Restaurar Contexto
                contexto_processo = contexto_salvo 
                
                log_eventos.append({
                    "tempo": relogio,
                    "tipo": "RETORNO",
                    "mensagem": f"Interrupção finalizada. Restaurando contexto (PC={contexto_processo}).",
                    "contexto": contexto_processo
                })

        else:
            # 3. Execução Normal
            contexto_processo += 1 
            log_eventos.append({
                "tempo": relogio,
                "tipo": "EXECUCAO",
                "mensagem": "Processo Principal em execução (CPU Ocupada).",
                "contexto": contexto_processo
            })
            relogio += 1

    # Evento final
    log_eventos.append({
        "tempo": relogio,
        "tipo": "FIM",
        "mensagem": "Tempo limite atingido. Simulação encerrada.",
        "contexto": contexto_processo
    })

    # --- GERAR ARQUIVO DE TEXTO ---
    try:
        with open("log_simulacao.txt", "w", encoding="utf-8") as arquivo:
            arquivo.write(f"=== RELATÓRIO DE SIMULAÇÃO ===\n")
            arquivo.write(f"Tempo Total Configurado: {tempo_total}\n")
            arquivo.write(f"Probabilidade: {probabilidade_interrupcao}%\n")
            arquivo.write("-" * 60 + "\n")
            
            for item in log_eventos:
                # Formata a linha como: [Tempo 10] [INTERRUPCAO] Mensagem...
                linha = f"[Tempo {item['tempo']}] [{item['tipo']}] {item['mensagem']} | Contexto: {item['contexto']}\n"
                arquivo.write(linha)
                
        print("Arquivo 'log_simulacao.txt' gerado com sucesso!")
    except Exception as e:
        print(f"Erro ao salvar arquivo de log: {e}")
    # -----------------------------------------------------------

    return {
        "log": log_eventos,
        "total_ciclos": relogio,
        "instrucoes_executadas": contexto_processo
    }