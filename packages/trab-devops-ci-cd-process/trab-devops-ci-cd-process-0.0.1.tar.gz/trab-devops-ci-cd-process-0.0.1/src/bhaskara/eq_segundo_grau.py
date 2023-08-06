# Este codigo encontra as raízes de uma equação de 2° grau: ax^2 + bx + c = 0

# commit versão_0 "codigo que calcula raízes de uma eq 2o grau"
# commit versão_1 "inclusao de condicao que exige coeficiente a <> 0"
# commit versão_2 "uso da fc os.system() para limpar a tela do terminal"

import math
import os


def incognitas(a, b, c):
    print("\nA eq. 2ºgrau {}x^2 + {}x + ({}) =0".format(a, b, c))
    delta = b**2 - 4*a*c

    if delta < 0:
        print("não possui raízes reais.")
        x1 = x2 = None
    elif delta == 0:
        x1 = (-b + math.sqrt(delta)) / (2*a)
        x2 = x1
        print("possui apenas uma raiz real: ", x1)
    else:
        x1 = (-b + math.sqrt(delta)) / (2*a)
        x2 = (-b - math.sqrt(delta)) / (2*a)
        print("possui duas raízes reais: \nx1 = {} \nx2 = {}".format(x1, x2))

    return (x1, x2)


def coleta_coeficientes():

    os.system('cls' if os.name == 'nt' else 'clear')
    print("Este codigo encontra as raízes de uma equação de 2° grau:\n\
ax^2 + bx + c = 0")

    a = float(input("\nDigite o valor de a: "))
    while a == 0:
        print("Valor de a invalido, digite um valor para 'a' \
diferente de zero: ")
        a = float(input("\nDigite o valor de a: "))
    b = float(input("Digite o valor de b: "))
    c = float(input("Digite o valor de c: "))

    incognitas(a, b, c)


# coleta_coeficientes()
