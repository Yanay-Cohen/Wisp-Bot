import aiorcon

class MinecraftBridge:
    def __init__(self, server_address, server_port, rcon_password):
        self.server_address = server_address
        self.server_port = server_port
        self.rcon_password = rcon_password
        self.rcon = None

    async def connect(self):
        self.rcon = aiorcon.Client(self.server_address, self.server_port, self.rcon_password)
        await self.rcon.connect()

    async def send_message(self, message):
        if not self.rcon:
            await self.connect()
        await self.rcon.send_cmd(f'say {message}')

    async def get_player_count(self):
        if not self.rcon:
            await self.connect()
        response = await self.rcon.send_cmd('list')
        # Typical response: "There are 2 of a max of 20 players online: player1, player2"
        try:
            count = int(response.split("There are ")[1].split(" of")[0])
            return count
        except Exception:
            return None

    async def close(self):
        if self.rcon:
            await self.rcon.close()
            self.rcon = None

    # Listening for Minecraft chat is not possible via RCON alone.
    # You'd need a plugin/mod or log tailing for that.