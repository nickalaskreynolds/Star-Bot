"""Embeds for Logging/Listeners Hub."""

# internal modules

# external modules
import discord

# relative modules
from .colours import Colours
from .embed_general import generic_embed
from .functions import current_time

# global attributes
__all__ = ('joinembed',
           'leaveembed',
           'usernameupdateembed',
           'roleaddembed',
           'roleremoveembed',
           'messageeditembed',
           'messagedeleteembed',
           'voicechannelstateembed',
           'voicechannelmoveembed',
           'kickembed',
           'logbanembed',
           'banembed',
           'unbanembed',
           'modembed',)
__filename__ = __file__.split('/')[-1].strip('.py')
__path__ = __file__.strip('.py').strip(__filename__)


def joinembed(joining_user: discord.User):
    """Embed for user onjoin event.

    Parameters
    ----------
    joining_user: discord.User
        discord object of user

    Returns
    -------
    discord.Embed
        embedded object to send message
    """
    ctitle = f'User joined'
    cdesc = f'{joining_user.name}#{joining_user.discriminator}'\
        f'\n\n{joining_user.id}'
    ccolors = Colours.Colours.CHANGE_G
    return generic_embed(ctitle, cdesc, [], current_time(), ccolour)[0].set_thumbnail(url=joining_user.avatar_url)


def leaveembed(leaving_user: discord.User):
    """Embed for user onleave event.

    Parameters
    ----------
    leaving_user: discord.User
        discord object of user

    Returns
    -------
    discord.Embed
        embedded object to send message
    """
    ctitle = f'User left'
    cdesc = f'{leaving_user.name}#{leaving_user.discriminator}'\
        f'\n\n{leaving_user.id}'
    ccolors = Colours.CHANGE_G
    return generic_embed(ctitle, cdesc, [], current_time(), ccolour)[0].set_thumbnail(url=leaving_user.avatar_url)


def usernameupdateembed(updated_user: discord.User, old_name: str, new_name: str):
    """Embed for user usernameupdate event.

    Parameters
    ----------
    updated_user: discord.User
        discord object of user
    old_name: str
        old username
    new_name: str
        new username

    Returns
    -------
    discord.Embed
        embedded object to send message
    """
    ctitle = f'Username changed'
    cdesc = f'{updated_user.name}#{updated_user.discriminator}'\
                 f' | {updated_user.id}'\
                 f'**Old**:\n{old_name}\n'\
                 f'**New**:\n{new_name}'
    ccolors = Colours.CHANGE_U
    return generic_embed(ctitle, cdesc, [], current_time(), ccolour)[0].set_thumbnail(url=joining_user.avatar_url)


def roleaddembed(updated_user: discord.User, role_name: str):
    """Embed for user roleadded event.

    Parameters
    ----------
    updated_user: discord.User
        discord object of user
    role_name: str
        role name added

    Returns
    -------
    discord.Embed
        embedded object to send message
    """
    ctitle = f'Role Added To User:'
    cdesc = f'{updated_user.name}#{updated_user.discriminator}'\
                 f' | {updated_user.id}\n'\
                 f'*{role_name}*'
    ccolors = Colours.CHANGE_U
    return generic_embed(ctitle, cdesc, [], current_time(), ccolour)[0]


def rolermembed(updated_user: discord.User, role_name: str):
    """Embed for user roleremoved event.

    Parameters
    ----------
    updated_user: discord.User
        discord object of user
    role_name: str
        role name removed

    Returns
    -------
    discord.Embed
        embedded object to send message
    """
    ctitle = f'Role Removed From User:'
    cdesc = f'{updated_user.name}#{updated_user.discriminator}'\
                 f' | {updated_user.id}\n'\
                 f'*{role_name}*'
    ccolors = Colours.CHANGE_U
    return generic_embed(ctitle, cdesc, [], current_time(), ccolour)[0]


def messageeditembed(message_user: discord.User, old_message: str, new_message: str, channel_name: str):
    """Embed for message edit event.

    Parameters
    ----------
    message_user: discord.User
        discord object of user
    old_message: str
        message prior to edit
    new_message: str
        message ante-edit
    channel_name: str
        channel name

    Returns
    -------
    discord.Embed
        embedded object to send message
    """
    ctitle = f'Message updated in {channel_name}'
    cdesc = f'{message_user.name}#{message_user.discriminator}'\
                 f' | {message_user.id}\n'\
                 f'**Old**:\n{old_message}\n'\
                 f'**New**:\n{new_message}'
    ccolors = Colours.CHANGE_M
    return generic_embed(ctitle, cdesc, [], current_time(), ccolour)[0]


def messagedeleteembed(message_user: discord.User, old_message: str, channel_name: str):
    """Embed for user message delete event.

    Parameters
    ----------
    message_user: discord.User
        discord object of user
    old_message: str
        message prior to delete
    channel_name: str
        channel name

    Returns
    -------
    discord.Embed
        embedded object to send message
    """
    ctitle = f'Message deleted in {channel_name}'
    cdesc = f'{message_user.name}#{message_user.discriminator}'\
                 f' | {message_user.id}\n'\
                 f'\n**Message**: {old_message}'
    ccolors = Colours.CHANGE_M
    return generic_embed(ctitle, cdesc, [], current_time(), ccolour)[0]


def voicechannelstateembed(channel_user: discord.User, action: str, channel_name: str):
    """Embed for user voice channel join/leave event.

    Parameters
    ----------
    channel_user: discord.User
        discord object of user
    action: str
        action of the user
    channel_name: str
        channel name

    Returns
    -------
    discord.Embed
        embedded object to send message
    """
    ctitle = 'Presence Update'
    cdesc = f'**{channel_user.name}#{channel_user.discriminator}**'\
                 f' has {action} **{channel_name}**.'
    ccolors = Colours.CHANGE_S
    return generic_embed(ctitle, cdesc, [], current_time(), ccolour)[0]


def voicechannelmoveembed(channel_user: discord.User, before_channel: str, after_channel: str):
    """Embed for user voice channel move event.

    Parameters
    ----------
    channel_user: discord.User
        discord object of user
    before_channel: str
        channel prior move
    after_channel: str
        channel ante-move

    Returns
    -------
    discord.Embed
        embedded object to send message
    """
    ctitle = f'Presence update moved channels'
    cdesc = f'**{channel_user.name}#{channel_user.discriminator}**'\
                 f'**Old**:\n{before_channel}\n'\
                 f'**New**:\n{after_channel}'
    ccolors = Colours.CHANGE_S
    return generic_embed(ctitle, cdesc, [], current_time(), ccolour)[0]

"""
GUILD ACTIONS
"""


def kickembed(kicked_name: str, kicked_id: str, mod_name: str,
                mod_id: str, reason: str):
    """Kick user.

    Parameters
    ----------
    kicked_name: str
        name of user
    kicked_id: str
        nid of user
    mod_name: str
        name of mod
    mod_id: str
        id of mod
    reason: str
        reason for ban

    Returns
    -------
    discord.Embed
        embedded object to send message
    """
    local_title = f'{kicked_name}: <@{kicked_id}> was '\
                  f'kicked by {mod_name}: <@{mod_id}>'
    local_desc = f'Reason: {reason}'
    ccolour = Colours.CHANGE_G
    return generic_embed(ctitle, cdesc, [], current_time(), ccolour)[0]


def logbanembed(banned_name: str, banned_id: str, mod_name: str,
                mod_id: str, reason: str):
    """Logban user.

    Parameters
    ----------
    banned_name: str
        name of user
    banned_id: str
        nid of user
    mod_name: str
        name of mod
    mod_id: str
        id of mod
    reason: str
        reason for ban

    Returns
    -------
    discord.Embed
        embedded object to send message
    """
    local_title = f'User Banned'
    cdesc = f'{banned_name}: <@{banned_id}> was '\
            f'banned by {mod_name}: <@{mod_id}>'\
            f'Reason: {reason}'
    ccolour = Colours.CHANGE_G
    return generic_embed(ctitle, cdesc, [], current_time(), ccolour)[0]


def banembed(*args, **kwargs):
    """User banned.

    Just calls :func: logbanembed

    Parameters
    ----------

    Returns
    -------
    discord.Embed
        embedded object to send message
    """
    return LogBanEmbed(*args, **kwargs)


def unbanembed(unbanned_name: str, unbanned_id: str, mod_name: str,
               mod_id: str, reason: str):
    """Ban removed.

    Parameters
    ----------
    unbanned_name: str
        name of user
    unbanned_id: str
        nid of user
    mod_name: str
        name of mod
    mod_id: str
        id of mod
    reason: str
        reason for ban

    Returns
    -------
    discord.Embed
        embedded object to send message
    """
    local_title = f'User Unbanned'
    cdesc = f'{unbanned_name}: <@{unbanned_id}> was '\
            f'unbanned by {mod_name}: <@{mod_id}>'\
            f'Reason: {reason}'
    ccolour = Colours.CHANGE_G
    return generic_embed(ctitle, cdesc, [], current_time(), ccolour)[0]


def modembed(modded_name: str, modded_id: str, mod_name: str, mod_id: str,
             action_type: ModAction, reason: str):
    """Moderation applied.

    Parameters
    ----------
    modded_name: str
        name of the user
    modded_id: str
        id of the user
    mod_name: str
        name of the mod
    mod_id: str
        id of the mod
    action_type: :func: ModAction
        The action type that describes this infraction
    reason: str
        reason for the modaction

    Returns
    -------
    discord.Embed
        embedded object to send message
    """
    ctitle = f'User Moderated'
    cdesc = f'{modded_name}: <@{modded_id}> was moderated '\
            f'({action_type.name})'\
            f'by {mod_name}: <@{mod_id}> \n'\
            f'Reason: {reason}'
    ccolour = Colours.CHANGE_G
    return generic_embed(ctitle, cdesc, [], current_time(), ccolour)[0]

# end of code

# end of file
