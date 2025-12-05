import random

def simular_entrada_saida(tempo_total, probabilidade_interrupcao, eventos_programados=None):
    """
    Simula o escalonamento de E/S com prioridades.
    Permite injeção de eventos para testes determinísticos.
    """
    
    dispositivos = [
        {"nome": "Teclado", "prioridade": 3, "tipo": "Alta", "tempo_tratamento": 2},
        {"nome": "Impressora", "prioridade": 2, "tipo": "Média", "tempo_tratamento": 4},
        {"nome": "Disco", "prioridade": 1, "tipo": "Baixa", "tempo_tratamento": 5},
    ]

    contexto_processo = 0
    log_eventos = []
    ciclos = 0

    log_eventos.append({
        "tempo": ciclos,
        "tipo": "INFO",
        "mensagem": "Início da simulação. Processo Principal carregado.",
        "contexto": contexto_processo,
    })

    if eventos_programados is None:
        eventos_programados = {}

    while ciclos < tempo_total:

        interrupcoes_neste_ciclo = []

        
        if ciclos in eventos_programados:
            nomes_devices = eventos_programados[ciclos]
            for nome in nomes_devices:
                dev = next((d for d in dispositivos if d["nome"] == nome), None)
                if dev:
                    interrupcoes_neste_ciclo.append(dev)
        
        elif random.randint(1, 100) <= probabilidade_interrupcao:
            interrupcoes_neste_ciclo.append(random.choice(dispositivos))
            if random.randint(1, 100) <= 30:
                interrupcoes_neste_ciclo.append(random.choice(dispositivos))

        if interrupcoes_neste_ciclo:
            
            nomes_chegaram = [d['nome'] for d in interrupcoes_neste_ciclo]
            if len(nomes_chegaram) > 1:
                 log_eventos.append({
                    "tempo": ciclos,
                    "tipo": "ALERTA",
                    "mensagem": f"CONFLITO DETECTADO: Múltiplas interrupções simultâneas {nomes_chegaram}",
                    "contexto": contexto_processo
                })

            interrupcoes_neste_ciclo.sort(key=lambda x: x["prioridade"], reverse=True)

            for i, dispositivo in enumerate(interrupcoes_neste_ciclo):
                
                msg_decisao = f"Iniciando tratamento de {dispositivo['nome']} (Prio {dispositivo['prioridade']})"
                
                if i > 0:
                    msg_decisao += " [Retirado da fila de espera]"

                log_eventos.append({
                    "tempo": ciclos,
                    "tipo": "INTERRUPCAO",
                    "mensagem": f"{msg_decisao}. Salvando contexto...",
                    "contexto": contexto_processo,
                })

                contexto_salvo = contexto_processo
                tempo_tratamento = dispositivo["tempo_tratamento"]

                log_eventos.append({
                    "tempo": ciclos + 1,
                    "tipo": "TRATAMENTO",
                    "mensagem": f"Processando {dispositivo['nome']} (Duração: {tempo_tratamento} ciclos)...",
                    "contexto": "Kernel/Driver",
                })

                ciclos += tempo_tratamento 

                contexto_processo = contexto_salvo

                log_eventos.append({
                    "tempo": ciclos,
                    "tipo": "RETORNO",
                    "mensagem": f"Tratamento de {dispositivo['nome']} finalizado. Restaurando contexto.",
                    "contexto": contexto_processo,
                })

        else:
            contexto_processo += 1
            log_eventos.append({
                "tempo": ciclos,
                "tipo": "EXECUCAO",
                "mensagem": "CPU Executando Processo Usuario.",
                "contexto": contexto_processo,
            })
            ciclos += 1

    # Fim da simulação
    log_eventos.append({
        "tempo": ciclos,
        "tipo": "FIM",
        "mensagem": "Tempo limite atingido. Simulação encerrada.",
        "contexto": contexto_processo,
    })

    try:
        nome_arquivo = "log_simulacao.txt"
        with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
            arquivo.write(f"=== RELATÓRIO DE SIMULAÇÃO (Engenharia de Software) ===\n")
            arquivo.write(f"Tempo Total: {tempo_total} ciclos\n")
            arquivo.write(f"Modo: {'Teste Controlado' if eventos_programados else 'Aleatório'}\n")
            arquivo.write("-" * 80 + "\n")

            for item in log_eventos:
                linha = f"[Tempo {item['tempo']:02d}] [{item['tipo']:<12}] {item['mensagem']}\n"
                arquivo.write(linha)

        print(f"\nSucesso! O arquivo '{nome_arquivo}' foi gerado.")
    except Exception as e:
        print(f"Erro ao salvar arquivo: {e}")

    return {"log": log_eventos}

