from ui import print_screen
from globals import *
from settings import *
import re

async def trim_emoji(full_name, short_name, string):
    return string.replace(full_name, ":" + short_name + ":")

async def convert_bold(string):
    sections = string.split("**")
    left = sections[0]
    target = sections[1]
    right = "".join(sections[2])
    return term.normal + left + " " + term.bold(target) + term.normal + " " + right

async def convert_italic(string):
    sections = string.split("*")
    left = sections[0]
    target = sections[1]
    right = "".join(sections[2])
    return term.normal + left + " " + term.italic(target) + term.normal + " " + right

async def calc_mutations(msg):

    # if the message is a file, extract the discord url from it
    try:
        json = str(msg.attachments[0]).split("'")
        msg.content = json[5]
        return msg
    
    # # otherwise it must not have any attachments and its a regular message
    except:
        text = msg.content

        # check to see if it has any custom-emojis
        # These will look like <:emojiname:39432432903201>
        # We will recursively trim this into just :emojiname:
        if msg.server.emojis is not None and len(msg.server.emojis) > 0:
            for emoji in msg.server.emojis:
                full_name = "<:" + emoji.name + ":" + emoji.id + ">" 
                                    
                while full_name in text:
                    text = await trim_emoji(full_name, emoji.name, text)

            msg.content = text

        # check for boldened font
        if text.count("**") > 1:
            while("**") in text:
                text = await convert_bold(text)            

            msg.content = text

        # check for italic font
        if text.count("*") > 1:
            while("*") in text:
                text = await convert_italic(text)            

            msg.content = text


        
        # check for italicized font
        


        return msg




async def on_incoming_message(msg):

    # TODO: make sure it isn't a private message

    # find the server/channel it belongs to and add it
    for server_log in server_log_tree:
        if server_log.get_server() == msg.server:
            for channel_log in server_log.get_logs():
                if channel_log.get_channel() == msg.channel:
                    channel_log.append(await calc_mutations(msg))
                    break

    # redraw the screen
    await print_screen()