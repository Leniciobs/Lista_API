from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
  return 'Bem-vindo à sua API calculadora'

@app.route('/api/somar', methods=['GET'])
def somar():
  try:
    numero1 = float(request.args.get('numero1'))
    numero2 = float(request.args.get('numero2'))
    resultado = numero1 + numero2
    return jsonify({"operacao": "soma", "resultado": resultado}), 200
  except Exception as e:
    return jsonify({"erro": "Erro ao realizar a soma. Verifique os valores informados."}), 400

@app.route('/api/subtrair', methods=['GET'])
def subtrair():
  try:
    numero1 = float(request.args.get('numero1'))
    numero2 = float(request.args.get('numero2'))
    resultado = numero1 - numero2
    return jsonify({"operacao": "subtracao", "resultado": resultado}), 200
  except Exception as e:
    return jsonify({"erro": "Erro ao realizar a subtração. Verifique os valores informados."}), 400

@app.route('/api/multiplicar', methods=['GET'])
def multiplicar():
  try:
    numero1 = float(request.args.get('numero1'))
    numero2 = float(request.args.get('numero2'))
    resultado = numero1 * numero2
    return jsonify({"operacao": "multiplicacao", "resultado": resultado}), 200
  except Exception as e:
    return jsonify({"erro": "Erro ao realizar a multiplicação. Verifique os valores informados."}), 400

@app.route('/api/dividir', methods=['GET'])
def dividir():
  try:
    numero1 = float(request.args.get('numero1'))
    numero2 = float(request.args.get('numero2'))
    if numero2 == 0:
      return jsonify({"erro": "Divisão por zero não é permitida."}), 400
    resultado = numero1 / numero2
    return jsonify({"operacao": "divisao", "resultado": resultado}), 200
  except Exception as e:
    return jsonify({"erro": "Erro ao realizar a divisão. Verifique os valores informados."}), 400

if __name__ == '__main__':
  app.run(debug=True)
