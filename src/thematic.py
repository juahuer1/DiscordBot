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

        self.simpsons = {"channel": self.simpsons_channel_name, "path": self.simpsons_base_path, "og_path": self.simpsons_og_base_path, "silent": False}
        self.offtopic = {"channel": self.offtopic_channel_name, "path": self.offtopic_base_path, "og_path": self.offtopic_og_base_path, "silent": True}