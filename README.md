# DiscordBot
Bot temático de los Simpsons que permite reproducir audios almacenados en el servidor. Incluye comandos y un panel de audio.

![moe_al_habla](https://github.com/user-attachments/assets/13b72689-fa5c-4173-85f3-1e0f5ffeabbc)


Para la instalación sigue los pasos descritos a continuación.
## Creación del bot

Para crear un bot, necesitas configurar una aplicación en el [Developer Portal de Discord](https://discord.com/developers/applications). Aquí tienes los pasos básicos:

Ve al Developer Portal de Discord.
Crea una nueva aplicación.
Dirígete a la sección "Bot" y añade un bot a tu aplicación (normalmente se crea solo). Activa las siguientes opciones en Privileged Gateway Intents:
- Presence Intent
- Server Members Intent
- Message Content Intent

Asegúrate de que el bot tenga los permisos necesarios Auth2:

En scope:
- applications.commands
- bot

En bot:
- Administrator (No necesita muchos de los permisos, revisa que quieres hacer con el bot y marca los necesarios para tu caso)

Con el bot creado integralo en tu servidor de discord, por alguna de las opciones de instalación, en caso de usar el link, asegurate de que lleve las opciones de configuración.

## Clona el repositorio

## Requerimientos
Asegúrate de tener instalado Python y Pip. Puedes instalar las dependencias necesarias ejecutando el siguiente comando:

```sh
pip install aiohttp==3.9.5 aiosignal==1.3.1 attrs==23.2.0 cffi==1.16.0 discord.py==2.4.0 frozenlist==1.4.1 idna==3.7 multidict==6.0.5 pip==23.0.1 pycparser==2.22 PyNaCl==1.5.0 python-dotenv==1.0.1 setuptools==66.1.1 yarl==1.9.4
```

## Creación archivo .env

Crear un archivo .env en la raíz del proyecto que contenga los datos necesarios para el bot:


```
BOTTOKEN=XXXXXXXXXXXXXXXXXXXX
APPLICATIONID=XXXXXXXXXXXXXXXXXXXX
```

## Correr el bot

Se necesita de un servidor donde alojar el bot y haber realizado correctamente los pasos anteriores, para utilizarlo, hay que lanzar en el servidor el siguiente comando desde la raiz del proyecto:

python pibot.py

Si todo ha ido bien debería aparecer algo similar a esto:

```sh
python pibot.py
2024-07-23 19:49:32 INFO     discord.client logging in using static token
2024-07-23 19:49:33 INFO     discord.gateway Shard ID None has connected to Gateway (Session ID: XXXXXXXXXXXXXXXXXXXX).
Bot conectado como PiBot#XXXX
```






