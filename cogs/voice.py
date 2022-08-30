# the code for this module sucks right now ill fix it later

import discord, asyncio, youtube_dl
from functools import partial
from discord.ext import commands
from a.funcs import f
import a.constants as tt

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl = youtube_dl.YoutubeDL({
	'format': 'bestaudio/best',
	'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
	'restrictfilenames': True,
	'noplaylist': True,
	'nocheckcertificate': True,
	'ignoreerrors': False,
	'logtostderr': False,
	'quiet': True,
	'no_warnings': True,
	'default_search': 'auto',
	'source_address': '0.0.0.0'
})

class YTDLSource(discord.PCMVolumeTransformer):
	def __init__(self, source, *, data, volume=0.25):
		super().__init__(source, volume)
		self.data = data
		self.title = data.get('title')
		self.url = 'https://www.youtube.com/watch?v='+data.get('url')

	@classmethod
	async def from_url(cls, url, *, loop=None):
		loop = loop or asyncio.get_event_loop()
		data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))
		print(data)
		if 'entries' in data:
			data = data['entries'][0]
		return cls(discord.FFmpegPCMAudio(data['url'], **{'options': '-vn'}), data=data)

class voice(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.queue = {}

	@commands.command()
	async def join(self, ctx):
		if ctx.voice_client is not None:
			return await ctx.voice_client.move_to(ctx.author.voice.channel)
		elif ctx.author.voice:
			await ctx.author.voice.channel.connect()
		else:
			await ctx.send(tt.w+"you are not connected to a voice channel")

	#@commands.command()
	#async def local(self, ctx, *, query):
	#	source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
	#	ctx.voice_client.play(source, after=lambda e: print(f'Player error: {e}') if e else None)
	#	await ctx.send(f'Now playing: {query}')

	#@commands.command()
	#async def yt(self, ctx, *, url):
	#	async with ctx.typing():
	#		player = await YTDLSource.from_url(url, loop=self.bot.loop)
	#		ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)
	#	await ctx.send(f'Now playing: {player.title}')

	@commands.command()
	async def play(self, ctx, *, query):
		async with ctx.typing():
			player = await YTDLSource.from_url(query, loop=self.bot.loop)
			ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)
			ctx.voice_client.play()
		await ctx.send(tt.y+f'now playing **{player.title}** {player.url}')

	@commands.command()
	async def volume(self, ctx, volume:int):
		if ctx.voice_client is None:
			return await ctx.send(tt.w+"not connected to a voice channel.")
		ctx.voice_client.source.volume = volume/100
		await ctx.send(tt.y+f"set volume to {volume}%")

	@commands.command()
	async def stop(self, ctx):
		await ctx.voice_client.stop()

	@commands.command()
	async def disconnect(self, ctx):
		await ctx.voice_client.disconnect()

	@commands.command()
	async def pause(self, ctx):
		if ctx.voice_client.is_playing() and not ctx.voice_client.is_paused():
			await ctx.voice_client.pause()
			ctx.send("paused playback")
		else:
			ctx.send("audio is already paused")

	@commands.command()
	async def resume(self, ctx):
		if ctx.voice_client.is_paused():
			await ctx.voice_client.resume()
			ctx.send("resumed playback")
		else:
			ctx.send("audio is not paused")

	@play.before_invoke
	async def ensure_voice(self, ctx):
		if ctx.author.voice:
			if not ctx.voice_client:
				await ctx.author.voice.channel.connect()
			if ctx.voice_client.is_playing():
				ctx.voice_client.stop()
			else:
				return await ctx.voice_client.move_to(ctx.author.voice.channel)
		else:
			await ctx.send(tt.w+"you are not connected to a voice channel!")
			
async def setup(bot):
	await bot.add_cog(voice(bot))
