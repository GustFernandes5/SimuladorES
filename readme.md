# Simulador de Gerenciamento de Entrada e Saída com Interrupção

Este projeto simula o comportamento de um Sistema Operacional gerenciando interrupções de hardware, troca de contexto e prioridades de dispositivos.

## 🖥️ Como Usar o Simulador

### Configuração
1. **Duração da Simulação:** Defina por quantos ciclos de clock a CPU deve rodar (Ex: 30 ciclos).
2. **Probabilidade de Interrupção:** Defina a chance (em %) de um dispositivo solicitar atenção a cada ciclo.
3. **Iniciar:** Clique no botão "Iniciar Simulação".

### Análise do Log
O sistema exibirá uma tabela colorida indicando os eventos:

* 🔵 **EXECUCAO:** Indica que o processo principal está usando a CPU.
* 🔴 **INTERRUPCAO:** Indica que o hardware parou a CPU.
* 🟠 **TRATAMENTO:** Indica o tempo gasto pelo SO atendendo o dispositivo.
* 🟢 **RETORNO:** Indica a restauração do contexto original.

## 🛠️ Tecnologias Utilizadas

* **Backend:** Python 3, Flask.
* **Frontend:** HTML5, CSS3, JavaScript (Fetch API).
* **Conceitos de SO:** Vetor de Interrupções, Troca de Contexto, Prioridade de E/S.

## 🚀 Como Executar
Para rodar este projeto localmente:

1. Instale as dependências:
   ```bash
   pip install flask flask-cors
    ````

2.  Execute a aplicação:

    ```bash
    python app.py
    ```

3.  Acesse no navegador: `http://127.0.0.1:5000`

## 👥 Autores

  * **Gustavo Fernandes dos Anjos**
  * **Leonardo Gonçalves da Silva**

