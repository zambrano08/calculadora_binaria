from flask import Flask, render_template, request

app = Flask(__name__)

def calcular_operacion(n1, n2, tipo):
    if not n1 or not n2: return None
    
    if tipo == 'division':
        divisor_int = int(n2, 2)
        if divisor_int == 0: return "Error: División por cero."
        
        dividendo_str = n1
        cociente = ""
        residuo_actual = ""
        pasos = []
        
        for bit in dividendo_str:
            anterior = residuo_actual
            residuo_actual += bit
            val_actual = int(residuo_actual, 2)
            
            if val_actual >= divisor_int:
                cociente += "1"
                resta = val_actual - divisor_int
                # Guardamos el estado antes de la resta para la visualización
                pasos.append({
                    "sustraendo": n2.rjust(len(residuo_actual), '0'),
                    "resultado": bin(resta)[2:].rjust(len(residuo_actual), '0'),
                    "visible": True
                })
                residuo_actual = bin(resta)[2:]
            else:
                cociente += "0"
        
        return {
            "dividendo": n1,
            "divisor": n2,
            "cociente": cociente.lstrip('0') or "0",
            "pasos": pasos,
            "residuo_final": residuo_actual,
            "tipo": "div"
        }

    # Lógica simplificada para las otras 3 operaciones
    max_l = max(len(n1), len(n2))
    a_p, b_p = n1.zfill(max_l), n2.zfill(max_l)
    res, p_sup = [], []

    if tipo == 'suma':
        c = 0
        for i in range(max_l-1, -1, -1):
            s = int(a_p[i]) + int(b_p[i]) + c
            res.insert(0, str(s%2)); p_sup.insert(0, str(c) if c>0 else " "); c = s//2
        if c: res.insert(0, str(c)); p_sup.insert(0, str(c))
        sig = "+"
    elif tipo == 'resta':
        if int(n1, 2) < int(n2, 2): return "Error: El primer número debe ser mayor."
        p = 0
        for i in range(max_l-1, -1, -1):
            r = int(a_p[i]) - int(b_p[i]) - p
            if r < 0: r+=2; p_sup.insert(0, "1"); p=1
            else: p_sup.insert(0, " "); p=0
            res.insert(0, str(r))
        sig = "-"
    else: # Multiplicación
        r_i = int(n1,2)*int(n2,2); r_b = bin(r_i)[2:]; t_c = len(r_b); prods = []
        for i, bit in enumerate(reversed(n2)):
            parc = n1 if bit == '1' else '0'*len(n1)
            prods.append(list(parc.zfill(len(parc)+i).rjust(t_c, ' ')))
        return {"bits_a": list(n1.rjust(t_c, ' ')), "bits_b": list(n2.rjust(t_c, ' ')), "productos": prods, "resultado": list(r_b), "total_cols": t_c, "signo": "x", "tipo": "mult"}

    t_c = len(res)
    return {"bits_a": list(a_p.zfill(t_c)), "bits_b": list(b_p.zfill(t_c)), "pasos": p_sup if len(p_sup)==t_c else [" "]+p_sup, "resultado": res, "total_cols": t_c, "signo": sig, "tipo": "std"}

@app.route('/', methods=['GET', 'POST'])
def index():
    proc, error = None, None
    if request.method == 'POST':
        res = calcular_operacion(request.form.get('num1',''), request.form.get('num2',''), request.form.get('operacion'))
        if isinstance(res, str): error = res
        else: proc = res
    return render_template('index.html', proc=proc, error=error)

if __name__ == '__main__':
    app.run(debug=True) 