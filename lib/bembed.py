import discord
from lib.colors import colors    # import color dict
import validators       # validation like url checking etc
import logging as log   # logging module

log.basicConfig(level=log.INFO, format='%(levelname)s: %(message)s')

if __name__ == 'lib.bembed':
    log.info('bembed.py loaded')

class Bembed:
    def __init__(self, type, title, description, color='red', url=None, bot=None, footer=None, footer_icon=None, author=None):
        log.debug(f'Bembed initialized with: type={type}, title={title}, description={description}, color={color}, url={url}, footer={footer}, author={author}')
        self.type = type
        self.title = title
        self.description = description
        self.color = self.get_color(color)
        self.url = url
        self.bot = bot
        self.author = author
        self.footer = footer
        self.footer_icon = footer_icon
        self.emb = self.blank_emb()
        self.fields = {}
        self.msg = None
        self.reactions = {}



    #
    #   Helper Functions
    #
    def blank_emb(self):
        if self.url:
            emb = discord.Embed(title=self.title, description=self.description, color=self.color, url=self.url)
        else:
            emb = discord.Embed(title=self.title, description=self.description, color=self.color)
        if self.author:
            if isinstance(self.author, dict): # check if author is dict
                try:
                    if validators.url(self.author['url']) and validators.url(self.author['icon']):
                        emb.set_author(name=self.author['name'], url=self.author['url'], icon_url=self.author['icon'])

                except KeyError:
                    try:
                        if validators.url(self.author['url']):
                            emb.set_author(name=self.author['name'], url=self.author['url'])
                    except KeyError:
                        emb.set_author(name=self.author['name'])
                # check if url and icon are url's and set the author
            if self.footer:
                self.emb.set_footer(text=footer)
        return emb

    # gets a name and returns color code
    def get_color(self, name):
        for c in colors:
            if c.lower() == name.lower():
                log.debug(f'get_color() returned color {c}')
                return colors[c] # return color from dict
        log.debug('get_color() default color returned')
        return 0xe74c3c # return red as default if none was found

    #
    #   Embed Functions
    #
    async def set_reactions(self):
        for react in self.reactions:
            try:
                await self.msg.add_reaction(react)
            except Exception as e:
                log.warning(e)
                return

    async def add_reaction(self, react, func=None):
        self.reactions[react] = func
        log.debug(self.reactions)
        await self.set_reactions()

    async def rem_reaction(self, react):
        self.reactions.pop(react)
        log.debug(self.reactions)
        await self.set_reactions()







    def set_fields(self, emb):
        for field in self.fields: # set all fields
            emb.add_field(name=field, value=self.fields[field][0], inline=self.fields[field][1])
        return emb

    # generates an new embed and send it:

    async def update(self, mode, content=None):
        # ------------------------------------------------------- #
        # -------------------- Generate Embed -------------------- #
        # ------------------------------------------------------- #
        local_cwd = __file__[:-13] # the folder above the lib folder
        old_type = self.type
        old_msg = self.msg
        emb = self.blank_emb()
        # --------- Fields --------- #
        # add one field to current fields. content needs to be a dict with {'name': ['value', inline (bool)]}
        if mode == 'addfields' or mode == 'addfield': # add one or multiple fields
            if not content:
                log.warning('specify the content! (field(s) to be added)')
                return
            if self.type == 'img':
                log.warning('cannot add fields to an image!')
                return
            if isinstance(content, dict):
                for field in content:  # add new fields to self.fields
                    self.fields[field] = content[field]
                emb = self.set_fields(emb)

        if mode == 'remfield': # remove a specific field
            if not content:
                log.warning('specify the content! (field to be removed)')
                return
            self.fields.pop(content) # remove field from self.fields
            emb = self.set_fields(emb)

        if mode == 'clearfields': # clear all fields
            self.fields = {}
        # --------- Image --------- #
        if mode == 'addimg':
            if not content:
                log.warning('specify the content! (image location)')
                return
            img_dir = local_cwd + content
            try:
                file = discord.File(img_dir, filename='img.png')
            except FileNotFoundError as e:
                log.warning(e)
                return
            emb.set_image(url="attachment://img.png")
            self.type = 'img'
            emb = self.set_fields(emb)

        if mode == 'remimg':
            self.type = 'txt'
            emb = self.set_fields(emb)

        if mode == 'addthb':
            if not content or:
                log.warning('specify the content! (image location)')
                return
            if not type =='txt':
                log.warning('you can only add a thumbnail to a txt embed')
                return
            img_dir = local_cwd + content
            try:
                file = discord.File(img_dir, filename='img.png')
            except FileNotFoundError as e:
                log.warning(e)
                return
            emb.add_thumbnail(url="attachment://img.png")



        # ------------------------------------------------------- #
        # -------------------- Sending Embed -------------------- #
        # ------------------------------------------------------- #
        # send new msg if type is changed from txt to img (or vice versa)
        if self.type == 'img':
            self.emb = emb # write new emb
            await self.msg.delete()
            # send embed with file if it is img
            self.msg = await old_msg.channel.send(embed=self.emb, file=file)


        if old_type == self.type == 'txt': # if old and new type is txt
            self.emb = emb # write new emb
            await self.msg.edit(embed=self.emb) # edit embed



    async def send(self, channel):
        self.msg = await channel.send(embed=self.emb)
