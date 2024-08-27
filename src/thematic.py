import os
from dotenv import load_dotenv

class InitEnv():
    def __init__(self):
        load_dotenv()
        self.simpsons_channel_name = os.getenv('SIMPSONSCHANNELNAME')
        self.offtopic_channel_name = os.getenv('OFFTOPICCHANNELNAME')
        self.help_channel_name = os.getenv('HELPCHANNELNAME')

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
        self.help = {
            "channel": self.help_channel_name,
            "title": "Panel de ayuda a la utilización de PiBot",
            "comandos": """
            Los comandos del bot se utilizan escribiendo en cualquier canal de texto barra (/), aparece una lista de los comandos disponibles y al escribirlos aparece debajo su descripción junto a un pequeño ejemplo de uso. Aquí los volvemos a explicar algunos en más detalle:\n 
               **• /roll** - Tira N dados de N caras en este orden NdN (dados, caras) (Ex: /roll 3d6)\n
               **• /joined** - Fecha de inclusion de un miembro (Ex: /joined juanmingla)\n
               **• /bot** - Dice si el bot mola (Ex: /bot)\n
               **• /join** - Agrega el bot al chat silenciosamente (Ex: /join)\n
               **• /leave** - Elimina el bot del chat de audio (Ex: /leave)\n
               **• /audios** - Introuduce en el chat de texto un selector de audios que permite elegir uno y que el bot se una al canal de audio para reproducirlo (otra opción más interactiva es usar los paneles de audio) (Ex: /audios)\n
               **• /cool** - Dice si alguien mola (Ex: /cool Khrisleo)\n
               **• /upload** - Permite subir y almacenar audios en el servidor, arrastra el audio que desees y un selector te audará a elegir en que carpeta quieres almacenar el audio, IMPORTANTE dependiendo de el panel de audio donde lances el comando, lo subirás a Simpsons o a Offtopic, preferiblemente utiliza nombres separados por guiones y sin acentos ni caracteres extraños (Ex: /upload)\n
               **• /createfolder** - Permite crear una carpeta para almacenar audios, la carpeta se creará en un panel u otro (Simpsons u Offtopic) en función del panel donde se lance el comando (Ex: /createfolder)"\n
               **• /deletefolder** - SOLO elimina una carpeta del servidor de Offtopic independientemente de donde se lance, si quieres borrar un audio del canal de Los Simpsons contacta con Sergio o Juan (Ex: /deletefolder)\n
               **• /clearaudio** - Interrumpimos audio que se esté reproduciendo (Ex: /clearaudio)\n
            """,
            "help_panel_command_path": "./Imagenes/Help/comandos.png",
                         "help_panel_command_name": "comandos.png",
                         "help_panel_command_url": "attachment://comandos.png",
            "paneles": """
               Hay dos paneles de audio, uno correspondiente a audios relacionados con Los Simpsons y otro llamado Offtopic donde se pueden subir audios de cualquier índole. Los usuarios pueden crear carpetas con el comando /createfolder mencionado anteriormente y aparecera un nuevo botón en el panel que se haya creado la carpeta, al clicar en cada uno de estos botones aparecerá un selector de audios para reproducir. Estos audios se pueden subir a la carpeta con el comando /upload
            """,
            "help_panel_panel_path": "./Imagenes/Help/paneles.png",
                         "help_panel_panel_name": "paneles.png",
                         "help_panel_panel_url": "attachment://paneles.png",
        }