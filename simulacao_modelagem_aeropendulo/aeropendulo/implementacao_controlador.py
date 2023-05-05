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

class ControladorDiscreto:
    """
        Classe que implementa os controladores para o sistema.
    """
    def __init__(self, referencia=1, T=0.0625):
        self.uk = 0
        self.uk1 = 0
        self.ek = 0
        self.ek1 = 0
        self.yout = 0
        self.k = 0
        self.r = referencia
        self.T = T

    # Pega o sinal do sensor
    def set_sensor(self, yout):
        self.yout = yout

    # disponibiliza o sinal de controle
    def get_u(self):
        """
            Método que retorna o sinal de controle.
        Returns:
            float.
        """
        return self.uk

    # Calcula o sinal de controle Proporcional Integral.
    def control_pi(self):
        """
        Método que implementa o controle Proporcional Integral discretizado.
        Returns:
            None.
        """
        self.ek = self.r - self.yout
        self.uk = self.uk1 + 0.2165 * self.ek - 0.2087 * self.ek1
        self.ek1 = self.ek
        self.uk1 = self.uk
        self.k = self.k + 1

    def controle_proporcional(self, kp=1.0):
        """
        Método que implementa o controle Proporcional.
        Returns:
            None.
        """
        self.ek = self.r - self.yout
        self.KP = kp
        self.uk = self.KP * self.ek
