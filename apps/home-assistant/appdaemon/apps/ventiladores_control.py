import appdaemon.plugins.hass.hassapi as hass
from datetime import datetime
import math

class VentiladoresControl(hass.Hass):

    def initialize(self):
        self.log("Inicializando VentiladoresControl")
        self.ventiladores = {
            #"ventilador1": {
            #    "velocidad_entity": "input_number.velocidad_ventilador1",
            #    "broadlink_device": "broadlink_rm_pro_1",
            #    "comando_base": "ventilador1_velocidad_"
            #},
            # ... (otros ventiladores)
        }

        for ventilador, config in self.ventiladores.items():
            self.log("Inicializando un Ventilador")
            self.listen_state(self.cambiar_velocidad, config["velocidad_entity"], ventilador=ventilador)
            self.log(f"Configurado listener para {ventilador}: {config['velocidad_entity']}")

    def cambiar_velocidad(self, entity, attribute, old, new, kwargs):
        ventilador = kwargs["ventilador"]
        self.log(f"Cambiando velocidad de {ventilador}: {old} -> {new}")
        config = self.ventiladores[ventilador]
        velocidad_porcentaje = float(new)
        velocidad_broadlink = self.mapear_velocidad(velocidad_porcentaje)
        self.log(f"Velocidad mapeada para {ventilador}: {velocidad_broadlink}")
        self.enviar_comando_broadlink(ventilador, velocidad_broadlink)

    def mapear_velocidad(self, velocidad_porcentaje):
        return math.ceil(velocidad_porcentaje / 100 * 5) + 1

    def enviar_comando_broadlink(self, ventilador, velocidad):
        config = self.ventiladores[ventilador]
        comando = f"{config['comando_base']}{velocidad}"
        self.log(f"Enviando comando para {ventilador}: {comando}")
        self.call_service("broadlink/send", device=config["broadlink_device"], command=comando)

    def termination(self):
        self.log("Terminando VentiladoresControl")