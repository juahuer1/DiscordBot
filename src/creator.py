import discord

class Creator:
	def view (timeout = 180, buttons = None, select = None):
		my_view = discord.ui.View (timeout = timeout)
		if buttons:
			my_view.add_item (buttons)
		if select:
			my_view.add_item (select)
			print("selectea")

	# def embed (self, embed):
	# 	my_embed = discord.Embed()

	# def select (self, select):
	# 	my_select = discord.ui.Select.super().__init__() #Aqui van las opciones

	# async def selectcallback():

	# def button (self, button):
	# 	my_button = discord.ui.Button()

	# async def buttoncallback():

	async def play (self, audio_selected):

		if not discord.VoiceClient.is_connected():
			await discord.VoiceChannel.connect

		source = FFmpegPCMAudio(audio_selected)
		discord.VoiceClient.play(source)