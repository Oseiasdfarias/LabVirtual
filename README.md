# LabVirtual

Compartilhamos aqui alguns conteúdos que estamos desenvolvendo buscando formatar um laboratório virtual para sistemas dinâmicos e controle na Faculdade de Engenharia Elétrica da UFPA-Tucuruí.

## Ferramentas do nosso interesse:

- [Python](https://www.python.org/) : Junto com os pacotes [Numpy](https://numpy.org/), [SciPy](https://scipy.org/) e [Matplotlib](https://matplotlib.org/) formam nossa base para programação.

- [VScode](https://code.visualstudio.com/) : A nossa IDE de programação e interface entre o computador e o GitHub. 

- [Manim](https://www.manim.community/) : Pacote de animação para matemática/ciência/engenharia - Integração com LaTeX.

- [PyMunk](https://www.pymunk.org/en/latest/) :

- [vPython](https://vpython.org/) : Simulação 3D;


## Conteúdo em desenvolvimento:

[Simulação de sistema dinâmico com python](Notas\IntegracaoNumerica\ManimEDO.html)

## Sistemas de interesse:

Sistemas possíveis:
- 1 - [Maglev](/labvirtual/simulacao_maglev/README.md)
- 4 - [Aeropêndulo](/labvirtual/simulacao_modelagem_aeropendulo/aeropendulo_doc.html)
   

## Exemplo de uso:


### Exemplo Maglev

```python
# -----------------------------------------------------
# Universidade Federal do Pará
# Campus Universitário de Tucuruí
# Faculdade de Engenharia Elétrica
# -----------------------------------------------------
#
# Laboratório Virtual Sistemas Dinâmicos e Controle
# Simulador: Maglev
# Autor: Yuri Cota
# Orientadores: Prof. Dr: Raphael Teixeira,
#               Prof. Dr: Rafael Bayma
#
# Data: 2023
#  ----------------------------------------------------
#
# Bibliotecas
import time

import numpy as np
from scipy.integrate import solve_ivp
import vpython as vp

# Importando o Modelo Matemático do Maglev
from labvirtual.simulador_maglev import Maglev

# Importando o Compensador
from labvirtual.simulador_maglev import Compensador

# Importando Simulador e Gráfico
from labvirtual.simulador_maglev import Simulacao
from labvirtual.simulador_maglev import Grafico


def run_maglev():
    # Criação dos objetos da planta e controlador para simular
    mag = Maglev(m=29e-3, k=9.55e-6, mu=2.19e-3, I0=1)
    comp = Compensador(mag, [-3*mag.lamda]*3, [-8*mag.lamda]*2)

    # Criando um Objeto Simulacao
    sim = Simulacao(mag_x0=mag.x0)

    grafico = Grafico()

    # Definindo os sinais de referência para rastreamento
    def ref_seno(t):
        return (mag.x0*np.sin(2*vp.pi*t))

    def ref_quad(t):
        return (mag.x0)*(np.sin(2*vp.pi*t) >= 0)

    # Função para ajustar coordenadas do modelo às coordenadas do VPython
    def converte_posicao(y_maglev):
        return (sim.bobina_3.pos + vp.vec(0, -y_maglev, 0))*4

    # Função para implementar ruído gaussiano
    def ruido(amp):
        return amp*np.random.normal(loc=0, scale=amp)

    # LOOP -------------------------------------------------------------------
    # Criando o loop da simulação
    while True:
        vp.rate(sim.fps)
        # Verificação da posição do cilindro antes de executar o programa
        if sim.cil.pos == vp.vector(12e-2, -3.5e-2, 0):
            grafico.legenda_1.text = "<b>O cilindro está na posição inicial!</b>"
            grafico.legenda_1.color = vp.color.green
        elif sim.cil.pos == vp.vector(0, 0, 0):
            grafico.legenda_1.text = "<b>Cilindo grudado!</b>"
            grafico.legenda_1.color = vp.color.red
        elif sim.cil.pos.y <= 0 and sim.cil.pos.y >= -0.08 and sim.cil.pos.x == 0:
            grafico.legenda_1.text = "<b>O cilindro está na região de equilíbrio!</b>"
            grafico.legenda_1.color = vp.color.cyan
        else:
            grafico.legenda_1.text = "<b>O cilindro está fora da região de equilíbrio!</b>"
            grafico.legenda_1.color = vp.color.purple

        # Acionando o botão executar
        if sim.executar:
            # O primeiro caso: se o cilindro está na posição inicial o
            # programa não vai sair da tela inicial.
            if sim.cil.pos == vp.vector(12e-2, -3.5e-2, 0):
                sim.cil.pos = vp.vector(12e-2, -3.5e-2, 0)
                grafico.yplot.delete()
                grafico.rplot.delete()
                sim.t = 0
                # time.sleep(2)
                sim.executar = not sim.executar
                sim.bt1_exe.text = "Executar"

            #  O segundo caso: o cilindro está grudado no eletroimã,
            # tem que aguardar o programa voltar pra tela inicial.
            elif sim.cil.pos == vp.vector(0, 0, 0):
                time.sleep(3)
                sim.executar = not sim.executar
                sim.bt1_exe.text = "Executar"
                sim.cil.pos = vp.vector(12e-2, -3.5e-2, 0)

            # O terceiro caso: o cilindro está na região 
            # de equilíbrio, logo o programa irá rodar normalmente.
            elif sim.cil.pos.y <= 0 and sim.cil.pos.y >= -0.08 and sim.cil.pos.x == 0:

                # Atualiza o sinal de referência para enviar para o solver
                match sim.M.index:
                    case 0 | None:
                        def sinal(t):
                            return ref_seno(sim.sl.value*sim.t)*(sim.sl2.value)
                    case 1:
                        def sinal(t):
                            return ref_quad(sim.sl.value*sim.t)*(sim.sl2.value)

                # Chama o solver para atualizar os estados do maglev
                sol = solve_ivp(Maglev.estadosmf, t_span=[
                                sim.t, sim.t+sim.dt], y0=sim.y,
                                args=(sinal, mag, comp))

                # Recupera os resultados da simulação
                sim.y = sol.y[:, -1]+ruido(1e-6)

                # Atualiza os gráficos
                grafico.yplot.plot(sim.t, sim.y[0])
                grafico.rplot.plot(sim.t, sinal(sim.t)+mag.x0)
                # print(y[0])

                # Atualiza a posição do cilindro
                sim.cil.pos = converte_posicao(sim.y[0])

                # Atualiza o tempo
                sim.t += sim.dt
    # O quarto caso: o cilindro está fora da região de equilíbrio, logo ele irá cair na mesa e retornar a posição inicial.
            else:
                while sim.cil.pos.y >= -3.5e-2:
                    vp.rate(sim.fps)
                    sim.cil.v = sim.cil.v+sim.g*sim.dt
                    sim.cil.pos = sim.cil.pos+sim.cil.v*sim.dt
                    sim.t = sim.t+sim.dt
                grafico.legenda_1.text = "<b>Aguarde o cilindro retonar a posição incial!</b>"
                grafico.legenda_1.color = vp.color.red
                time.sleep(4)
                sim.cil.pos = vp.vector(12e-2, -3.5e-2, 0)
                print(sim.t)


if __name__ == "__main__":
    run_maglev()
```

### Exemplo Aeropêndulo

```python
# -----------------------------------------------------
# Universidade Federal do Pará
# Campus Universitário de Tucuruí
# Faculdade de Engenharia Elétrica
# -----------------------------------------------------
#
# Laboratório Virtual Sistemas Dinâmicos e Controle
# Simulador: Aeropêndulo
# Autor: Oséias Farias
# Orientadores: Prof. Dr: Raphael Teixeira,
#               Prof. Dr: Rafael Bayma
#
# Data: 2023
#  ----------------------------------------------------
#

import vpython as vp
import numpy as np
from labvirtual.simulador_aeropendulo import (Graficos, AnimacaoAeropendulo,
                                              Interface, ModeloMatAeropendulo,
                                              ControladorDiscreto)


def run_aeropendulo():
    # Instanciando um objeto AeropenduloAaeropendulo()
    animacao_aeropendulo = AnimacaoAeropendulo()

    # Instanciando um objeto para plotagem dos gráficos dinâmicos dos
    # estados do Aeropêndulo
    g = Graficos()
    graf, plot1, plot2, plot3, plot4 = g.graficos()

    # Instânciando um objeto para solução matemática do sistema Aeropêndulo.
    Km = 0.0296
    m = 0.36
    d = 0.03
    J = 0.0106
    c = 0.0076
    mma = ModeloMatAeropendulo(K_m=Km, m=m, d=d, J=J, c=c)

    # Instânciando um objeto ControladorDiscreto
    controlador = ControladorDiscreto(referencia=0.01)
    u = 0  # Sinal de controle inicial

    # Instanciando um objeto Interface
    interface = Interface(animacao_aeropendulo, controlador)

    ts = 1e-2
    # Condições Iniciais dos estados
    x = np.array([0.0, 0.0])
    t = 0.0
    t_ant = 0.0

    # Simulação do Sistema
    while True:
        vp.rate(100)
        if interface.EXE:
            # Calcula as derivadas do sitema
            dx = mma.modelo_aeropendulo(x, t)
            dt = t - t_ant

            # Atualização dos estados
            x = x + dt * dx

            # Pega o Ângulo e envia para o controlador
            # (Realimentação do sistema)
            controlador.set_sensor(x[1])

            # O controlador calcula o sinal de controle
            controlador.control_pi()

            # Controle proporcional
            # controlador.controle_proporcional(kp=10.0)
            # pega o sinal de controle calculado e salva na variável u
            u = controlador.get_u()

            # Sinal de controle aplicado a entrada do sistema
            mma.set_u(u)

            # print(x[1]*(180/np.pi))
            t_ant = t
            t += ts

            # Atualiza o ângulo do Aeropêndulo
            animacao_aeropendulo.aeropendulo.rotate(axis=vp.vec(0, 0, 1),
                                                    angle=x[0]*ts,
                                                    origin=vp.vec(0, 5.2, 0))

            # Animação da dinâmica da Hélice
            animacao_aeropendulo.update_helice(x[0], ts)

            # print(x[1] + interface.valor_angle)
            # Gráfico do ângulo.
            plot1.plot(t, x[1] + interface.valor_angle)
            # Gráfico do sinal de referência
            plot2.plot(t, controlador.r + interface.valor_angle)
            # Gráfico da velocidade ângular.
            plot3.plot(t, x[0])
            # Gráfico do sinal de controle
            plot4.plot(t, u)


if __name__ == "__main__":
    run_aeropendulo()
```