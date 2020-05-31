import datetime

PRECO_LITRO_COMBUSTIVEL = 1.5  # Euros
CONSUMO_LITROS_100_KM = 6  # litros / 100 km

HORAS_DIA = 24
MINUTOS_HORA = 60
SEGUNDOS_MINUTO = 60


class Viagem:

    def __init__(self):
        self.tempo_decorrido = datetime.time(0, 0, 0)
        self.dias_decorridos = 0
        self.distancia_percorrida = 0.0
        self.local_actual = ""
        self.modo_actual = ""

    def set_tempo(self, tempo):
        self.tempo_decorrido = tempo

    def set_dias(self, dias):
        self.dias_decorridos = dias

    def set_distancia(self, distancia):
        self.distancia_percorrida = distancia

    def set_local(self, local):
        self.local_actual = local

    def set_modo(self, modo):
        self.modo_actual = modo

    def add_tempo(self, tempo_extra):
        horas = self.tempo_decorrido.hour
        minutos = self.tempo_decorrido.minute
        segundos = self.tempo_decorrido.second

        segundos += tempo_extra.second
        if segundos >= SEGUNDOS_MINUTO:
            minutos += 1
            segundos -= SEGUNDOS_MINUTO
        minutos += tempo_extra.minute
        if minutos >= MINUTOS_HORA:
            horas += 1
            minutos -= MINUTOS_HORA
        horas += tempo_extra.hour
        if horas >= HORAS_DIA:
            self.dias_decorridos += 1
            horas -= HORAS_DIA

        self.tempo_decorrido = datetime.time(horas, minutos, segundos)

    def add_distancia(self, distancia_extra):
        self.distancia_percorrida += distancia_extra

    def get_tempo(self):
        return self.tempo_decorrido

    def get_dias(self):
        return self.dias_decorridos

    def get_distancia(self):
        return self.distancia_percorrida

    def get_local(self):
        return self.local_actual

    def get_modo(self):
        return self.modo_actual

    def get_consumo_combustivel(self):
        return CONSUMO_LITROS_100_KM * (self.distancia_percorrida / 100)

    def get_dinheiro_gasto(self):
        return self.get_consumo_combustivel() * PRECO_LITRO_COMBUSTIVEL
