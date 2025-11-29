from flask import Flask, render_template, request, jsonify
from simulate import simular_entrada_saida
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Rota para carregar a página
@app.route('/')
def index():
    return render_template('index.html')

# Rota da API (Recebe JSON, Retorna JSON)
@app.route('/simular', methods=['POST'])
def simular():
    try:
        data = request.json
        
        # Coleta parâmetros do usuário
        tempo_simulacao = int(data.get('tempo_simulacao', 20))
        probabilidade = int(data.get('probabilidade', 30))
        
        # Validação simples
        if tempo_simulacao <= 0 or probabilidade < 0 or probabilidade > 100:
            return jsonify({"erro": "Parâmetros inválidos. Verifique os valores."}), 400

        # Chama o motor
        resultado = simular_entrada_saida(tempo_simulacao, probabilidade)
        
        return jsonify(resultado)

    except Exception as e:
        return jsonify({"erro": f"Erro interno: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True)