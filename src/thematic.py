import os
from dotenv import load_dotenv

class InitEnv:
   load_dotenv()
   simpsons_channel_name = os.getenv('SIMPSONSCHANNELNAME')
   offtopic_channel_name = os.getenv('OFFTOPICCHANNELNAME')
   help_channel_name = os.getenv('HELPCHANNELNAME')

   simpsons_og_base_path = os.getenv('SIMPSONSORIGINALPATH')
   simpsons_base_path = os.getenv('SIMPSONSPATH')
   offtopic_og_base_path = os.getenv('OFFTOPICORIGINALPATH')
   offtopic_base_path = os.getenv('OFFTOPICPATH')

   simpsons = {"channel": simpsons_channel_name, 
                   "path": simpsons_base_path, 
                   "og_path": simpsons_og_base_path, 
                   "silent": False,
                   "audio_panel_title": "Bar de Moe, Moe al habla",
                   "audio_panel_description": [
                      "*¿Señor Reves? de nombre Stal*, \n Un momento, A VEEER STAL REVES, alguno de ustedes Stal Reves?",
                      "*¿Está Topocho? De nombre Donpi* \n Deja que pregunte. Donpi Topocho, ¿ES QUE NADIE AQUÍ ES UN DONPI TOPOCHO?",
                      "*¿Está el señor Riau? De nombre Smith* \n Un momento, voy a ver. ¿Hay aquí algún Smith Riau? ¿NO ME OÍS? ¿¡ALGUNO SOIS SMITH RIAU!?",
                      "*¿Está Empel? De nombre Otas* \n Voy a ver. ¡QUE SE PONGA AL TELÉFONO EMPEL OTAS!",
                      "*Pregunto por el señor Ollas, de nombre Philip* \n Sí, un minuto, voy a ver. PHILIP OLLAS, PHILIP OLLAS. Venga, chicos, ¿no hay ningún Philip Ollas por aquí?",
                      "*Quisiera hablar con la señora Chondo. ¿De nombre? Stoika* \n Un segundo. STOIKA CHONDO, STOIKA CHONDO. Vamos, señora, creo que esto va por usted ¡STOIKA CHONDO!"
                   ],
                   "audio_panel_image_path": "./Imagenes/Simpsons/moe_al_habla.jpg",
                   "audio_panel_image_name": "moe_al_habla.jpg",
                   "audio_panel_image_url": "attachment://moe_al_habla.jpg"
                   }
   offtopic = {"channel": offtopic_channel_name, 
                   "path": offtopic_base_path, 
                   "og_path": offtopic_og_base_path, 
                   "silent": True,
                   "audio_panel_title": "Panel de audios y ya", 
                   "audio_panel_description": [
                      "Panel de audios donde puedes crear y subir audios para reproducirlos durante las llamadas de discord (Comandos mkdir y upload respectivamente)."
                   ],
                   "audio_panel_image_path": "./Imagenes/Offtopic/offtopic.jpg",
                   "audio_panel_image_name": "offtopic.jpg",
                   "audio_panel_image_url": "attachment://offtopic.jpg"
                  }
   helper = {
      "channel": help_channel_name,
      "title": "Panel de ayuda a la utilización de PiBot",
      "comandos": """
      Escribe barra (/) en cualquier canal de texto para ver una lista de comandos disponibles con una descripción y un ejemplo.\n 
         **• /roll** - Tira *times* dados de *faces* caras (Ex: /roll 3d6)\n
         **• /joined** - Fecha de inclusion de un miembro (Ex: /joined juanmingla)\n
         **• /bot** - Dice si el bot mola (Ex: /bot)\n
         **• /join** - Agrega el bot al chat silenciosamente (Ex: /join)\n
         **• /leave** - Elimina el bot del chat silenciosamente (Ex: /leave)\n
         **• /audios** - Elige y reproduce un audio [Se recomienda usar los Paneles] (Ex: /audios)\n
         **• /cool** - Dice si alguien mola (Ex: /cool Khrisleo)\n
         **• /upload** - Sube un audio al Panel en el que te encuentres. Separa las palabras con guiones y evita acentos u otros caracteres extraños (Ex: /upload)\n
         **• /createfolder** - Crea una carpeta en el Panel en el que te encuentres (Ex: /createfolder)\n
         **• /delete** - SOLO elimina una carpeta o audio de Offtopic. Si quieres que sea en Los Simpsons contacta con Sergio o Juan (Ex: /delete)\n
         **• /clearaudio** - Interrumpimos audio que se esté reproduciendo (Ex: /clearaudio)\n
      """,
      "help_panel_command_path": "./Imagenes/Help/comandos.png",
      "help_panel_command_name": "comandos.png",
      "help_panel_command_url": "attachment://comandos.png",
      "paneles": """
         **audio-panel** está dedicado a Los Simpsons exclusivamente \n
         **audio-panel-offtopic** recoge audios de cualquier otra temática \n
         Utiliza */createfolder* para añadir botones y llénalos de audios con */upload*
      """,
      "help_panel_panel_path": "./Imagenes/Help/paneles.png",
      "help_panel_panel_name": "paneles.png",
      "help_panel_panel_url": "attachment://paneles.png",
   }