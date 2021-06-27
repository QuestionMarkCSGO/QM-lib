import discord
from colors import colors    # import color dict
from icons import icons    # import icon dict
import validators       # validation like url checking etc
import logging as log   # logging module

log.basicConfig(level=log.INFO, format='%(levelname)s: %(message)s')

if __name__ == 'lib.bembed':
    log.info('bembed.py loaded')

class Bembed:
    def __init__(self, bot, type='txt', title='Embed Title', description='', color='red', url=None, footer=None, footer_icon=None, author=None):
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
        self.is_send = False



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
    async def delete_msg():
        await self.msg.delete()
    # add reaction to embed msg.
    # usage: await self.add_reaction({'react': ['type', func]})
    # react -> emoji
    # type -> 'stay': the reaction of any user will stay or 'remove': the reaction will be deleted so there should be only one react on every emoji
    # func -> you can give a function wich will be called when someone reacts on this emoji or use a keyword:
    # func keywords:
    # 'delete' -> delete the message
    async def add_reaction(self, react, type='stay', func=None):
        if not callable(func):
            if func == 'delete':
                func = self.delete_msg
        self.reactions[react] = [type, func]
        log.info(f'{react} added')
        await self.set_reactions()

    async def rem_reaction(self, react):
        self.reactions.pop(react)
        log.info(f'{react} removed')
        log.debuglog(self.reactions)
        await self.set_reactions()


    def set_fields(self, emb):
        for field in self.fields: # set all fields
            emb.add_field(name=field, value=self.fields[field][0], inline=self.fields[field][1])
        return emb

    # generates an new embed and send it:
    # usage: await self.update('mode', content)
    # mode keywords:
    # addfield(s): adds one or multiple fields. content: {'name':['value', is_inline (True/False)]})
    # remfield: removes one field. content: 'name' (name of the field you added with addfield)
    # clearfields: removes all fields at once. Don't need content
    # addimg: set an image. content: path to image (relative to the cwd) or url to an image
    # remimg: set embed to text. Don't need content
    # addthb: set the thumbnail. content: path to image (relative to the cwd) or url to an image
    # remthb: removes the thumbnail. Don't need content
    async def update(self, mode, content=None):
        # check if embed is send
        if not self.is_send:
            log.warning('You need to send the Embed before updating it')
            return
        # ------------------------------------------------------- #
        # -------------------- Generate Embed -------------------- #
        # ------------------------------------------------------- #
        local_cwd = __file__[:-13] # the folder above the lib folder
        old_type = self.type
        old_msg = self.msg
        emb = self.blank_emb()
        # --------- Fields --------- #
        # add one field to current fields. content needs to be a dict with {'field_name': ['value', inline (bool)]}
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
            else:
                log.error('content needs to be a dict. ')
        # remove a specific field content: 'field_name'
        if mode == 'remfield':
            if not content:
                log.warning('specify the content! (field to be removed)')
                return
            self.fields.pop(content) # remove field from self.fields
            emb = self.set_fields(emb)

        # clears all fields
        if mode == 'clearfields':
            self.fields = {}
        # --------- Image --------- #
        # set embed image. content needs to be a local file inside the folder of your bot.py or an url to an image
        if mode == 'addimg':
            if not content:
                log.warning('specify the content! (image location)')
                return
            is_url = validators.url(content)
            if not is_url:
                print('Image is not url!')
                try:
                    img_dir = local_cwd + content
                    file = discord.File(img_dir, filename='img.png')
                    emb.set_image(url="attachment://img.png")
                except FileNotFoundError as e:
                    log.warning(e)
                    return
            else:
                print('Image is url!')
                emb.set_image(url=content)
            self.type = 'img'
            #emb = self.set_fields(emb)

        # remove the image
        if mode == 'remimg':
            self.type = 'txt'
            emb = self.set_fields(emb)

        # add a thumbnail to the embed. content needs to be a local file inside the folder of your bot.py or an url to an image
        if mode == 'addthb':
            if not content:
                log.warning('specify the content! (image location)')
                return
            if self.type !='txt':
                log.warning('you can only add a thumbnail to a txt embed')
                return
            is_url = validators.url(content)
            if not is_url:
                log.debug('Image is not url!')
                try:
                    img_dir = local_cwd + content
                    log.info(f'image dir: {img_dir}')
                    file = discord.File(img_dir, filename='img.png')
                    emb.set_thumbnail(url="attachment://img.png")
                except FileNotFoundError as e:
                    log.warning(e)
                    return
            else:
                log.debug('Image is url!')
                emb.set_thumbnail(url=content)




        # ------------------------------------------------------- #
        # -------------------- Sending Embed -------------------- #
        # ------------------------------------------------------- #
        # send new msg if type is changed from txt to img (or vice versa)
        self.emb = emb # write new emb
        if self.type == 'img':
            await self.msg.delete()
            if is_url:
                # send embed without file if it is a link
                self.msg = await old_msg.channel.send(embed=self.emb)
            else:
                # send embed with file if it is local img
                self.msg = await old_msg.channel.send(embed=self.emb, file=file)
        if old_type == self.type == 'txt': # if old and new type is txt edit the msg
            await self.msg.edit(embed=self.emb)

    async def set_info(self, title, text=' '):
        self.emb = discord.Embed(title=title, description=text, color=self.get_color('green'))
        self.emb.set_author(name='Info!', icon_url=icons['info'])

    async def set_warning(self, title, text=' '):
        self.emb = discord.Embed(title=title, description=text, color=self.get_color('yellow'))
        self.emb.set_author(name='Warning!', icon_url=icons['warning'])

    async def set_error(self, title, text=' '):
        self.emb = discord.Embed(title=title, description=text, color=self.get_color('red'))
        self.emb.set_author(name='Error!', icon_url=icons['error'])

    async def send(self, channel):
        try:
            self.msg = await channel.send(embed=self.emb)
            self.is_send = True
        except Exception as e:
            log.error(e)
            return
