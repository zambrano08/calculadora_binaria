from flask import Flask, render_template, request

app = Flask(__name__)

def calcular_operacion(n1, n2, tipo):
    if not n1 or not n2: return None
    
    # Lógica para DIVISIÓN
    if tipo == 'division':
        divisor_int = int(n2, 2)
        if divisor_int == 0: return "Error: No se puede dividir por cero."
        
        dividendo_str = n1
        divisor_str = n2
        cociente = ""
        residuo_actual = ""
        pasos_division = []
        
        for bit in dividendo_str:
            residuo_actual += bit
            val_actual = int(residuo_actual, 2)
            if val_actual >= divisor_int:
                cociente += "1"
                resta = val_actual - divisor_int
                pasos_division.append({
                    "sustraendo": divisor_str.rjust(len(residuo_actual), ' '),
                    "residuo": bin(resta)[2:].rjust(len(residuo_actual), ' ')
                })
                residuo_actual = bin(resta)[2:]
            else:
                cociente += "0"
        
        return {
            "dividendo": list(n1), "divisor": n2, "cociente": cociente.lstrip('0') or "0",
            "pasos": pasos_division, "residuo_final": residuo_actual, "tipo": "div"
        }

    # Lógica para MULTIPLICACIÓN
    if tipo == 'multiplicacion':
        res_int = int(n1, 2) * int(n2, 2)
        res_bin = bin(res_int)[2:]
        total_cols = len(res_bin)
        productos_parciales = []
        for i, bit in enumerate(reversed(n2)):
            parcial = n1 if bit == '1' else '0' * len(n1)
            fila = list(parcial.zfill(len(parcial) + i).rjust(total_cols, ' '))
            productos_parciales.append(fila)
        return {
            "bits_a": list(n1.rjust(total_cols, ' ')), "bits_b": list(n2.rjust(total_cols, ' ')),
            "productos_parciales": productos_parciales, "resultado": list(res_bin),
            "total_cols": total_cols, "signo": "x", "tipo": "mult"
        }

    # Lógica para SUMA y RESTA
    max_len = max(len(n1), len(n2))
    a_padded, b_padded = n1.zfill(max_len), n2.zfill(max_len)
    resultado, pasos = [], []

    if tipo == 'suma':
        acarreo = 0
        for i in range(max_len - 1, -1, -1):
            s = int(a_padded[i]) + int(b_padded[i]) + acarreo
            resultado.insert(0, str(s % 2))
            pasos.insert(0, str(acarreo) if acarreo > 0 else " ")
            acarreo = s // 2
        if acarreo:
            resultado.insert(0, str(acarreo))
            pasos.insert(0, str(acarreo))
        signo = "+"
    else:
        if int(n1, 2) < int(n2, 2): return "Error: El primer número debe ser mayor para la resta."
        prestamo = 0
        for i in range(max_len - 1, -1, -1):
            r = int(a_padded[i]) - int(b_padded[i]) - prestamo
            if r < 0:
                r += 2
                pasos.insert(0, "1")
                prestamo = 1
            else:
                pasos.insert(0, " ")
                prestamo = 0
            resultado.insert(0, str(r))
        signo = "-"

    t_cols = len(resultado)
    return {
        "bits_a": list(a_padded.zfill(t_cols)), "bits_b": list(b_padded.zfill(t_cols)),
        "pasos": pasos if len(pasos) == t_cols else [" "] + pasos,
        "resultado": resultado, "total_cols": t_cols, "signo": signo, "tipo": "std"
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    proc, error = None, None
    if request.method == 'POST':
        n1 = request.form.get('num1', '').strip()
        n2 = request.form.get('num2', '').strip()
        t = request.form.get('operacion')
        res = calcular_operacion(n1, n2, t)
        if isinstance(res, str): error = res
        else: proc = res
    return render_template('index.html', proc=proc, error=error)

if __name__ == '__main__':
    app.run(debug=True)