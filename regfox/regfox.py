from redbot.core import commands
from redbot.core import Config
from redbot.core.utils import chat_formatting
import aiohttp
from fake_useragent import UserAgent

class RegFox(commands.Cog):
    """RegFox cog, handles communication with RegFox registration platform"""
    def __init__(self, bot):
        self.config = Config.get_conf(self, identifier=3857064354, force_registration=True)
        default_guild = {
            "apiKey":"",
            "pageid":0
        }
        self.config.register_guild(**default_guild)
        self.bot = bot
        self.useragent = UserAgent()
        self.session = aiohttp.ClientSession('https://api.webconnex.com/v2/public')

    @commands.hybrid_command(name="setapikey")
    @commands.admin()
    async def setAPIKey(self,ctx,new_value):
        await self.config.guild(ctx.guild).apiKey.set(new_value)
        await ctx.send("RegFox API Key updated!")

    @commands.hybrid_command(name="setpageid")
    @commands.admin()
    async def setPageID(self,ctx,new_value):
        await self.config.guild(ctx.guild).pageid.set(new_value)
        await ctx.send("RegFox page ID updated!")

    @commands.hybrid_command(name="regcount")
    async def regcount(self,ctx):
        pageidconf = await self.config.guild(ctx.guild).pageid()
        apikeyconf = await self.config.guild(ctx.guild).apiKey()
        url = "/forms/{pageid}/inventory".format(pageid=pageidconf)
        headers = {
            "apiKey": "{}".format(apikeyconf),
            "User-Agent": self.useragent.random
        }
        try:
            async with session.get(url, headers=headers) as response:
                apidata = await response.json()
        except ConnectionError:
            await ctx.send("Connection error, unable to reach RegFox")
        else:
            if response.status == 200:
                await ctx.send("{count} currently registered!".format(count=apidata['data'][1]['sold']))
            else:
                errorfile = chat_formatting.text_to_file(response.text(),filename='error.txt',spoiler=False,encoding='utf-8')
                await ctx.send("ERROR {code}".format(code=response.status), file=errorfile)
    
    @commands.hybrid_command(name="connectiontest")
    @commands.admin()
    async def connectiontest(self,ctx):
        apikeyconf = await self.config.guild(ctx.guild).apiKey()
        url = "https://api.webconnex.com/v2/public/ping"
        headers = {
            "apiKey": "{}".format(apikeyconf),
            "User-Agent": self.useragent.random
        }
        try:
            async with session.get(url, headers=headers) as response:
                await apidata = response.json()
        except ConnectionError:
            await ctx.send("Connection error, unable to reach RegFox")
        else:             
            await ctx.send("Code {code}, MSG {data}".format(code=response.status, data=apidata['data']))