from flask import Flask, render_template, request

app = Flask(__name__)

def calcular_operacion(n1, n2, tipo):
    if not n1 or not n2: return None
    
    # Lógica de DIVISIÓN (Método de Restas Alineadas)
    if tipo == 'division':
        divisor_int = int(n2, 2)
        if divisor_int == 0: return "Error: División por cero."
        
        dividendo_str = n1
        cociente = ""
        residuo_actual = ""
        pasos_tabla = []
        
        for i, bit in enumerate(dividendo_str):
            anterior = residuo_actual
            residuo_actual += bit
            val_actual = int(residuo_actual, 2)
            
            paso = {"bajado": bit, "residuo_previo": anterior}
            
            if val_actual >= divisor_int:
                cociente += "1"
                resta = val_actual - divisor_int
                paso.update({
                    "sustraendo": n2.rjust(len(residuo_actual), '0'),
                    "resultado_resta": bin(resta)[2:],
                    "accion": "resta"
                })
                residuo_actual = bin(resta)[2:]
            else:
                cociente += "0"
                paso.update({"accion": "pasa"})
                
            pasos_tabla.append(paso)
            
        return {
            "dividendo": n1, "divisor": n2, "cociente": cociente.lstrip('0') or "0",
            "pasos": pasos_tabla, "residuo_final": residuo_actual, "tipo": "div"
        }

    # MULTIPLICACIÓN
    if tipo == 'multiplicacion':
        res_int = int(n1, 2) * int(n2, 2)
        res_bin = bin(res_int)[2:]
        total_cols = len(res_bin)
        productos = []
        for i, bit in enumerate(reversed(n2)):
            parcial = n1 if bit == '1' else '0' * len(n1)
            productos.append(list(parcial.zfill(len(parcial) + i).rjust(total_cols, ' ')))
        return {
            "bits_a": list(n1.rjust(total_cols, ' ')), "bits_b": list(n2.rjust(total_cols, ' ')),
            "productos": productos, "resultado": list(res_bin), "total_cols": total_cols, "signo": "x", "tipo": "mult"
        }

    # SUMA y RESTA
    max_len = max(len(n1), len(n2))
    a_padded, b_padded = n1.zfill(max_len), n2.zfill(max_len)
    resultado, pasos_sup = [], []

    if tipo == 'suma':
        acarreo = 0
        for i in range(max_len - 1, -1, -1):
            s = int(a_padded[i]) + int(b_padded[i]) + acarreo
            resultado.insert(0, str(s % 2))
            pasos_sup.insert(0, str(acarreo) if acarreo > 0 else " ")
            acarreo = s // 2
        if acarreo: resultado.insert(0, str(acarreo)); pasos_sup.insert(0, str(acarreo))
        signo = "+"
    else:
        if int(n1, 2) < int(n2, 2): return "Error: El primer número debe ser mayor."
        prestamo = 0
        for i in range(max_len - 1, -1, -1):
            r = int(a_padded[i]) - int(b_padded[i]) - prestamo
            if r < 0: r += 2; pasos_sup.insert(0, "1"); prestamo = 1
            else: pasos_sup.insert(0, " "); prestamo = 0
            resultado.insert(0, str(r))
        signo = "-"

    t_cols = len(resultado)
    return {
        "bits_a": list(a_padded.zfill(t_cols)), "bits_b": list(b_padded.zfill(t_cols)),
        "pasos": pasos_sup if len(pasos_sup) == t_cols else [" "] + pasos_sup,
        "resultado": resultado, "total_cols": t_cols, "signo": signo, "tipo": "std"
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    proc, error = None, None
    if request.method == 'POST':
        n1, n2, t = request.form.get('num1', '').strip(), request.form.get('num2', '').strip(), request.form.get('operacion')
        res = calcular_operacion(n1, n2, t)
        if isinstance(res, str): error = res
        else: proc = res
    return render_template('index.html', proc=proc, error=error)

if __name__ == '__main__':
    app.run(debug=True)