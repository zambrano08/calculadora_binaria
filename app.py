from flask import Flask, render_template, request

app = Flask(__name__)

def calcular_operacion(n1, n2, tipo):
    max_len = max(len(n1), len(n2))
    a_padded = n1.zfill(max_len)
    b_padded = n2.zfill(max_len)
    
    resultado = []
    pasos_superiores = [] # Acarreos o Préstamos
    
    if tipo == 'suma':
        acarreo = 0
        for i in range(max_len - 1, -1, -1):
            s = int(a_padded[i]) + int(b_padded[i]) + acarreo
            resultado.insert(0, str(s % 2))
            pasos_superiores.insert(0, str(acarreo) if acarreo > 0 else " ")
            acarreo = s // 2
        if acarreo:
            resultado.insert(0, str(acarreo))
            pasos_superiores.insert(0, str(acarreo))
        signo = "+"
    else:
        # Lógica de Resta (A - B)
        prestamo = 0
        # Convertimos a int para validar si el resultado será negativo
        if int(n1, 2) < int(n2, 2):
            return "Error: El primer número debe ser mayor o igual al segundo para este formato."
            
        for i in range(max_len - 1, -1, -1):
            bit_a = int(a_padded[i])
            bit_b = int(b_padded[i])
            
            resta = bit_a - bit_b - prestamo
            
            if resta < 0:
                resta += 2
                pasos_superiores.insert(0, "1")
                prestamo = 1
            else:
                pasos_superiores.insert(0, " ")
                prestamo = 0
            resultado.insert(0, str(resta))
        signo = "-"

    total_cols = len(resultado)
    # Alinear números al ancho del resultado
    return {
        "bits_a": list(a_padded.zfill(total_cols)),
        "bits_b": list(b_padded.zfill(total_cols)),
        "pasos": pasos_superiores if len(pasos_superiores) == total_cols else [" "] + pasos_superiores,
        "resultado": resultado,
        "total_cols": total_cols,
        "signo": signo
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    proc = None
    error = None
    if request.method == 'POST':
        n1 = request.form.get('num1', '').strip()
        n2 = request.form.get('num2', '').strip()
        tipo = request.form.get('operacion')
        if n1 and n2:
            res = calcular_operacion(n1, n2, tipo)
            if isinstance(res, str): error = res
            else: proc = res
    return render_template('index.html', proc=proc, error=error)

if __name__ == '__main__':
    app.run(debug=True)