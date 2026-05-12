from flask import Flask, render_template, request

app = Flask(__name__)

def suma_binaria_pasos(a, b):
    # Asegurar que tengan la misma longitud
    max_len = max(len(a), len(b))
    a = a.zfill(max_len)
    b = b.zfill(max_len)
    
    acarreo = 0
    pasos_acarreos = []
    resultado = []
    
    for i in range(max_len - 1, -1, -1):
        bit_a = int(a[i])
        bit_b = int(b[i])
        suma = bit_a + bit_b + acarreo
        
        res_bit = suma % 2
        pasos_acarreos.insert(0, str(acarreo))
        resultado.insert(0, str(res_bit))
        acarreo = suma // 2
        
    if acarreo:
        resultado.insert(0, str(acarreo))
        pasos_acarreos.insert(0, str(acarreo))
    else:
        pasos_acarreos.insert(0, " ")

    return {
        "a": a,
        "b": b,
        "acarreos": "".join(pasos_acarreos),
        "resultado": "".join(resultado)
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    procedimiento = None
    if request.method == 'POST':
        num1 = request.form.get('num1')
        num2 = request.form.get('num2')
        # Aquí puedes expandir para resta, mult, etc.
        procedimiento = suma_binaria_pasos(num1, num2)
    return render_template('index.html', proc=procedimiento)

if __name__ == '__main__':
    app.run(debug=True)