from flask import Flask, render_template, request

app = Flask(__name__)

def calcular_suma_binaria(a, b):
    max_len = max(len(a), len(b))
    a_padded = a.zfill(max_len)
    b_padded = b.zfill(max_len)
    
    acarreo = 0
    lista_acarreos = []
    resultado = []
    
    for i in range(max_len - 1, -1, -1):
        bit_a = int(a_padded[i])
        bit_b = int(b_padded[i])
        suma = bit_a + bit_b + acarreo
        
        res_bit = suma % 2
        # El acarreo actual se muestra sobre la columna actual
        lista_acarreos.insert(0, str(acarreo) if acarreo > 0 else " ")
        resultado.insert(0, str(res_bit))
        acarreo = suma // 2
        
    if acarreo:
        resultado.insert(0, str(acarreo))
        lista_acarreos.insert(0, str(acarreo))
    else:
        lista_acarreos.insert(0, " ")

    total_cols = len(resultado)
    # Ajustamos A y B al ancho del resultado para que no se muevan
    final_a = list(a_padded.zfill(total_cols))
    final_b = list(b_padded.zfill(total_cols))

    return {
        "bits_a": final_a,
        "bits_b": final_b,
        "bits_acarreos": lista_acarreos,
        "bits_resultado": resultado,
        "total_cols": total_cols
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    proc = None
    if request.method == 'POST':
        n1 = request.form.get('num1', '').strip()
        n2 = request.form.get('num2', '').strip()
        if n1 and n2:
            proc = calcular_suma_binaria(n1, n2)
    return render_template('index.html', proc=proc)

if __name__ == '__main__':
    app.run(debug=True)