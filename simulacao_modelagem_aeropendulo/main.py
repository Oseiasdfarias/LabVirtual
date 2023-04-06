# -----------------------------------------------------
# Universidade Federal do Pará
# Campus Universitário de Tucuruí
# Faculdade de Engenharia Elétrica
# -----------------------------------------------------
#
# Laboratório Virtual Sistemas Dinâmicos e Controle
# Tema: Simulação Aeropêndulo
# Autor: Oséias Farias
# Orientadores: Prof. Dr: Raphael Teixeira,
#               Prof. Dr: Rafael Bayma
#
# Data: 2023
#  ----------------------------------------------------
#
import vpython as vp
import numpy as np
from aeropendulo import (Graficos, AnimacaoAeropendulo,
                         Interface, ModeloMatAeropendulo,
                         ControladorDiscreto)

# Instanciando um objeto AeropenduloAaeropendulo = Aeropendulo()
animacao_aeropendulo = AnimacaoAeropendulo()

# Instanciando um objeto para plotagem dos gráficos dinâmicos dos
# estados do Aeropêndulo
g = Graficos()
graf, plot1, plot2, plot3, plot4 = g.graficos()

# Instânciando um objeto para solução matemática do sistema Aeropêndulo.
mma = ModeloMatAeropendulo()

# Instânciando um objeto ControladorDiscreto
controlador = ControladorDiscreto(referencia=0.1)  # np.pi/2.
u = 0  # Sinal de controle inicial

# Instanciando um objeto Interface
interface = Interface(animacao_aeropendulo, controlador)

ts = 1e-2
# Condições Iniciais dos estados
x = np.array([0.0, 0.0])
t = 0.0
t_ant = 0.0

helice = vp.box(pos=vp.vec(0.8, 0.6, 0), size=vp.vec(0.05, 0.2, 2),
                color=vp.vec(1, 1, 0))

helice1 = vp.box(pos=vp.vec(0.8, 0.6, 0), size=vp.vec(0.05, 0.2, 2),
                 color=vp.vec(1, 1, 0))
helice1.axis = animacao_aeropendulo.aeropendulo.axis
helice1.size = vp.vec(0.05, 0.2, 2)
helice1.rotate(axis=vp.vec(1, 0, 0),
               angle=vp.pi/4)

helice2 = vp.box(pos=vp.vec(0.8, 0.6, 0), size=vp.vec(0.05, 0.2, 2),
                 color=vp.vec(1, 1, 0))
helice2.axis = animacao_aeropendulo.aeropendulo.axis
helice2.size = vp.vec(0.05, 0.2, 2)
helice2.rotate(axis=vp.vec(1, 0, 0),
               angle=vp.pi/2)

helice3 = vp.box(pos=vp.vec(0.8, 0.6, 0), size=vp.vec(0.05, 0.2, 2),
                 color=vp.vec(1, 1, 0))
helice3.axis = animacao_aeropendulo.aeropendulo.axis
helice3.size = vp.vec(0.05, 0.2, 2)
helice3.rotate(axis=vp.vec(1, 0, 0),
               angle=3*vp.pi/4.)

# Simulação do Sistema
while True:
    vp.rate(100)
    if interface.EXE:
        # Calcula as derivadas do sitema
        dx = mma.modelo_aeropendulo(x, t)
        dt = t - t_ant

        # Atualização dos estados
        x = x + dt * dx

        # Pega o Ângulo e envia para o controlador (Realimentação do sistema)
        controlador.set_sensor(x[1])

        # O controlador calcula o sinal de controle
        controlador.calc_uk()

        # pega o sinal de controle calculado e salva na variável u
        u = controlador.get_uk()

        # Sinal de controle aplicado a entrada do sistema
        mma.set_u(u)

        # print(x[1]*(180/np.pi))
        t_ant = t
        t += ts
        # Atualiza o ângulo do Aeropêndulo

        animacao_aeropendulo.aeropendulo.rotate(axis=vp.vec(0, 0, 1),
                                                angle=x[0]*ts,
                                                origin=vp.vec(0, 5.2, 0))

# #################   DINÂMICAS DAS HÉLICES DO AEROPÊNDULO   ###############
        helice.size = vp.vec(0.05, 0.2, 2)
        helice1.size = vp.vec(0.05, 0.2, 2)
        helice2.size = vp.vec(0.05, 0.2, 2)
        helice3.size = vp.vec(0.05, 0.2, 2)
        helice.axis = animacao_aeropendulo.aeropendulo.axis
        helice1.axis = animacao_aeropendulo.aeropendulo.axis
        helice2.axis = animacao_aeropendulo.aeropendulo.axis
        helice3.axis = animacao_aeropendulo.aeropendulo.axis
        helice.size = vp.vec(0.05, 0.2, 2)
        helice1.size = vp.vec(0.05, 0.2, 2)
        helice2.size = vp.vec(0.05, 0.2, 2)
        helice3.size = vp.vec(0.05, 0.2, 2)
        helice.rotate(axis=vp.vec(0, 0, 1),
                      angle=x[0]*ts,
                      origin=vp.vec(0, 5.2, 0))
        helice1.rotate(axis=vp.vec(0, 0, 1),
                       angle=x[0]*ts,
                       origin=vp.vec(0, 5.2, 0))
        helice2.rotate(axis=vp.vec(0, 0, 1),
                       angle=x[0]*ts,
                       origin=vp.vec(0, 5.2, 0))
        helice3.rotate(axis=vp.vec(0, 0, 1),
                       angle=x[0]*ts,
                       origin=vp.vec(0, 5.2, 0))
        helice.size = vp.vec(0.05, 0.2, 2)
        helice1.size = vp.vec(0.05, 0.2, 2)
        helice2.size = vp.vec(0.05, 0.2, 2)
        helice3.size = vp.vec(0.05, 0.2, 2)

        # obs tentando ajustar o diro das hélices apenas para um lado ....
        if x[1] + interface.valor_angle < np.pi/2:
            ag = 0.3
        else:
            ag = -0.8

        helice.rotate(axis=vp.vec(1, 0, 0),
                      angle=0.1)
        helice1.rotate(axis=vp.vec(1, 0, 0),
                       angle=0.1)
        helice2.rotate(axis=vp.vec(1, 0, 0),
                       angle=0.1)
        helice3.rotate(axis=vp.vec(1, 0, 0),
                       angle=0.1)

# ##################   DINÂMICAS DAS HÉLICES DO AEROPÊNDULO   #################

        print(x[1] + interface.valor_angle)
        # Gráfico do ângulo.
        plot1.plot(t, x[1] + interface.valor_angle)
        # Gráfico do sinal de referência
        plot2.plot(t, controlador.r + interface.valor_angle)
        # Gráfico da velocidade ângular.
        plot3.plot(t, x[0])
        # Gráfico do sinal de controle
        plot4.plot(t, u)
