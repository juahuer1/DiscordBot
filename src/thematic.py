import os
from dotenv import load_dotenv

class InitEnv():
    def __init__(self):
        load_dotenv()
        self.simpsons_channel_name = os.getenv('SIMPSONSCHANNELNAME')
        self.offtopic_channel_name = os.getenv('OFFTOPICCHANNELNAME')

        self.simpsons_og_base_path = os.getenv('SIMPSONSORIGINALPATH')
        self.simpsons_base_path = os.getenv('SIMPSONSPATH')
        self.offtopic_og_base_path = os.getenv('OFFTOPICORIGINALPATH')
        self.offtopic_base_path = os.getenv('OFFTOPICPATH')

        self.simpsons = {"channel": self.simpsons_channel_name, 
                         "path": self.simpsons_base_path, 
                         "og_path": self.simpsons_og_base_path, 
                         "silent": False,
                         "audio_panel_title": "Bar de Moe, Moe al habla",
                         "audio_panel_description": [
                            "*¿Señor Reves? de nombre Stal*, \n Un momento, A VEEER STAL REVES, alguno de ustedes Stal Reves?",
                            "*¿Está Topocho? De nombre Donpi* \n Deja que pregunte. Donpi Topocho, ¿ES QUE NADIE AQUÍ ES UN DONPI TOPOCHO?",
                            "*¿Está el señor Riau? De nombre Smith* \n Un momento, voy a ver. ¿Hay aquí algún Smith Riau? ¿NO ME OÍS? ¿¡ALGUNO SOIS SMITH RIAU!?",
                            "*¿Está Empel? De nombre Otas* \n Voy a ver. ¡QUE SE PONGA AL TELÉFONO EMPEL OTAS!",
                            "*Pregunto por el señor Ollas, de nombre Philip* \n Sí, un minuto, voy a ver. PHILIP OLLAS, PHILIP OLLAS. Venga, chicos, ¿no hay ningún Philip Ollas por aquí?",
                            "*Quisiera hablar con la señora Chondo. ¿De nombre? Stoika \n Un segundo. STOIKA CHONDO, STOIKA CHONDO. Vamos, señora, creo que esto va por usted ¡STOIKA CHONDO!"
                         ],
                         "audio_panel_image_path": "./Imagenes/Simpsons/moe_al_habla.jpg",
                         "audio_panel_image_name": "moe_al_habla.jpg",
                         "audio_panel_image_url": "attachment://moe_al_habla.jpg"
                         }
        self.offtopic = {"channel": self.offtopic_channel_name, 
                         "path": self.offtopic_base_path, 
                         "og_path": self.offtopic_og_base_path, 
                         "silent": True,
                         "audio_panel_title": "Panel de audios y ya", 
                         "audio_panel_description": [
                            "Panel de audios donde puedes crear y subir audios para reproducirlos durante las llamadas de discord (Comandos mkdir y upload respectivamente)."
                         ],
                         "audio_panel_image_path": "./Imagenes/Offtopic/offtopic.jpg",
                         "audio_panel_image_name": "offtopic.jpg",
                         "audio_panel_image_url": "attachment://offtopic.jpg"
                        }