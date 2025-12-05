import random

def simular_entrada_saida(tempo_total, probabilidade_interrupcao):
    
    dispositivos = [
        {"nome": "Teclado", "prioridade": 3, "tipo": "Alta", "tempo_tratamento": 2},
        {"nome": "Impressora", "prioridade": 2, "tipo": "Média", "tempo_tratamento": 4},
        {"nome": "Disco", "prioridade": 1, "tipo": "Baixa", "tempo_tratamento": 5}
    ]

    contexto_processo = 0
    log_eventos = []
    relogio = 0
    
    log_eventos.append({
        "tempo": relogio,
        "tipo": "INFO",
        "mensagem": "Início da simulação. Processo Principal carregado.",
        "contexto": contexto_processo
    })

    while relogio < tempo_total:
        
        interrupcoes_neste_ciclo = []
        
        if random.randint(1, 100) <= probabilidade_interrupcao:
            dev = random.choice(dispositivos)
            interrupcoes_neste_ciclo.append(dev)
            
            if random.randint(1, 100) <= 30:
                dev2 = random.choice(dispositivos)
                interrupcoes_neste_ciclo.append(dev2)

        if interrupcoes_neste_ciclo:
            
            interrupcoes_neste_ciclo.sort(key=lambda x: x["prioridade"], reverse=True)
            
            for dispositivo in interrupcoes_neste_ciclo:
                
                log_eventos.append({
                    "tempo": relogio,
                    "tipo": "INTERRUPCAO",
                    "mensagem": f"Interrupção recebida ({dispositivo['nome']} - Prio: {dispositivo['tipo']}). Salvando contexto...",
                    "contexto": contexto_processo
                })
                
                contexto_salvo = contexto_processo 
                
                tempo_tratamento = dispositivo["tempo_tratamento"]
                log_eventos.append({
                    "tempo": relogio + 1,
                    "tipo": "TRATAMENTO",
                    "mensagem": f"Tratando requisição do {dispositivo['nome']} (Duração: {tempo_tratamento} ciclos)...",
                    "contexto": "Sistema Operacional"
                })
                
                relogio += tempo_tratamento
                
                contexto_processo = contexto_salvo 
                
                log_eventos.append({
                    "tempo": relogio,
                    "tipo": "RETORNO",
                    "mensagem": f"Interrupção finalizada. Restaurando contexto (PC={contexto_processo}).",
                    "contexto": contexto_processo
                })

        else:
            contexto_processo += 1 
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

    try:
        with open("log_simulacao.txt", "w", encoding="utf-8") as arquivo:
            arquivo.write(f"=== RELATÓRIO DE SIMULAÇÃO ===\n")
            arquivo.write(f"Tempo Total Configurado: {tempo_total}\n")
            arquivo.write(f"Probabilidade: {probabilidade_interrupcao}%\n")
            arquivo.write("-" * 60 + "\n")
            
            for item in log_eventos:

                linha = f"[Tempo {item['tempo']}] [{item['tipo']}] {item['mensagem']} | Contexto: {item['contexto']}\n"
                arquivo.write(linha)
                
        print("Arquivo 'log_simulacao.txt' gerado com sucesso!")
    except Exception as e:
        print(f"Erro ao salvar arquivo de log: {e}")

    return {
        "log": log_eventos,
        "total_ciclos": relogio,
        "instrucoes_executadas": contexto_processo
    }