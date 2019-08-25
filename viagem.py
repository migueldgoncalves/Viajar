import datetime

PRECO_LITRO_COMBUSTIVEL = 1.5  # Euros
CONSUMO_LITROS_100_KM = 6  # litros / 100 km


class Viagem:

    tempo_decorrido = datetime.time(0, 0, 0)
    distancia_percorrida = 0.0
    local_actual = ""

    def set_tempo(self, tempo):
        self.tempo_decorrido = tempo

    def set_distancia(self, distancia):
        self.distancia_percorrida = distancia

    def set_local(self, local):
        self.local_actual = local

    def add_tempo(self, tempo_extra):
        horas = self.tempo_decorrido.hour
        minutos = self.tempo_decorrido.minute
        segundos = self.tempo_decorrido.second
        horas += tempo_extra.hour
        minutos += tempo_extra.minute
        if minutos >= 60:
            horas += 1
            minutos -= 60
        segundos += tempo_extra.second
        if segundos >= 60:
            minutos += 1
            segundos -= 60
        self.tempo_decorrido = datetime.time(horas, minutos, segundos)

    def add_distancia(self, distancia_extra):
        self.distancia_percorrida += distancia_extra

    def get_tempo(self):
        return self.tempo_decorrido

    def get_distancia(self):
        return self.distancia_percorrida

    def get_local(self):
        return self.local_actual

    def get_consumo_combustivel(self):
        return CONSUMO_LITROS_100_KM * (self.distancia_percorrida / 100)

    def get_dinheiro_gasto(self):
        return self.get_consumo_combustivel() * PRECO_LITRO_COMBUSTIVEL
