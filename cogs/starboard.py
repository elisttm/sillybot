import nextcord, re
from nextcord.utils import get
from nextcord.ext import commands
from a.funcs import f
import a.constants as tt

class starboard(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.db = tt.db['starboard']
		self.re_img = re.compile(f"http(.*?)({'|'.join(tt.filetypes.img)})")

	def starboard_emoji(self, config, emo):
		x = config.get('starboardemoji','⭐')
		return (emo.name == x) if emo.is_unicode_emoji() else (emo.id == x)

	async def starboard_content(self, message, count):
		_attachments_ = ''.join([f"[{a.filename}]({a.url})\n" for a in message.attachments])
		e_sb = nextcord.Embed(description=f"{message.content}\n{_attachments_}\n[jump to message]({message.jump_url})", color=0xffac33, timestamp=message.created_at)
		e_sb.set_author(name=f"{message.author.name}#{message.author.discriminator}", icon_url=message.author.avatar.url)
		e_sb.set_footer(text=f"{message.id}")
		if len(message.attachments) != 0 and '.'+message.attachments[0].url.rsplit('.',1)[1] in tt.filetypes.img:
			e_sb.set_image(url=message.attachments[0].url)
		else:
			img = self.re_img.search(message.content)
			if img != None:
				e_sb.set_image(url="http"+img.group(1)+img.group(2))
		return [f"{tt.e.star3 if count >= 10 else tt.e.star2 if count > 5 else tt.e.star} **{count}** {message.channel.mention}", e_sb]

	@commands.Cog.listener()
	async def on_raw_reaction_add(self, payload):
		if payload.member.bot or (nextcord.utils.utcnow()-nextcord.Object(payload.message_id).created_at).days >= 7:
			return
		message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
		config = tt.config.find_one({'_id':message.guild.id},{'starboard':1,'starboardcount':1,'starboardemoji':1})
		if not config:
			return
		if 'starboard' in config and self.starboard_emoji(config, payload.emoji):
			reaction = get(message.reactions, emoji=payload.emoji.name if payload.emoji.is_unicode_emoji() else payload.emoji)
			if reaction.count >= int(config['starboardcount']) if 'starboardcount' in config else 5:
				content = await self.starboard_content(message, reaction.count)
				stored = self.db.find_one({'_id':message.id},{'_id':0})
				if stored != None:
					if stored['channel'] != config['starboard']:
						self.db.delete_one({'_id':message.id})
						return
					boardmsg = await self.bot.get_channel(config['starboard']).fetch_message(stored['board'])
					if content[0] != boardmsg.content or content[1] != boardmsg.embeds[0]:
						await boardmsg.edit(content=content[0], embed=content[1])
				else:
					boardmsg = await self.bot.get_channel(config['starboard']).send(content=content[0], embed=content[1])
					self.db.update_one({'_id':message.id}, {"$set":{'board':boardmsg.id,'channel':config['starboard'],'date':message.created_at}}, upsert=True)

	@commands.Cog.listener()
	async def on_raw_reaction_remove(self, payload):
		if (nextcord.utils.utcnow()-nextcord.Object(payload.message_id).created_at).days >= 7:
			return
		message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
		config = tt.config.find_one({'_id':message.guild.id},{'starboard':1,'starboardcount':1,'starboardemoji':1})
		if not config:
			return
		if self.starboard_emoji(config, payload.emoji):
			reaction = get(message.reactions, emoji=payload.emoji.name if payload.emoji.is_unicode_emoji() else payload.emoji)
			stored = self.db.find_one({'_id':message.id},{'_id':0})
			if stored != None and reaction != None:
				if stored['channel'] != config['starboard']:
					self.db.delete_one({'_id':message.id})
					return
				try:
					boardmsg = await self.bot.get_channel(config['starboard']).fetch_message(stored['board'])
					content = await self.starboard_content(message, reaction.count)
					if content[0] != boardmsg.content and content[1] != boardmsg.embeds[0]:
						await boardmsg.edit(content=content[0], embed=content[1])
				except:
					self.db.delete_one({'_id':message.id})

def setup(bot):
	bot.add_cog(starboard(bot))
