"""Embeds for Moderation Hub."""

# internal modules

# external modules
import discord

# relative modules
from .colours import Colours
from .functions import ModAction, current_time
from .embed_general import generic_embed

# global attributes
__all__ = ('untimeout',
           'timeout',
           'warningeditembed',
           'warningaddembed',
           'warningrmembed',
           'warninglistembed',
           'modlistembed',
           'modeditembed',
           'modaddembed',
           'modrmembed')
__filename__ = __file__.split('/')[-1].strip('.py')
__path__ = __file__.strip('.py').strip(__filename__)

"""
TIMEOUT
"""


def untimeout(user_name: str, user_id: str, mod_name: str, mod_id: str,
              channel: bool, role: bool, category: bool, perms_removed: list):
    """Timeout removed.

    Parameters
    ----------
    user_name: str
        name of the user
    user_id: str
        id of the user
    mod_name: str
        name of the mod
    mod_id: str
        id of the mod
    channel: bool
        if perms describe roles
    role: bool
        if perms describe channels
    category: bool
        if perms describe categories
    perms_removed: list
        list[id] of the target perms

    Returns
    -------
    discord.Embed
        embedded object to send message
    """
    ctitle = f'User Removed From Time Out'
    cdesc = f'{user_name}: <@{user_id}> has been removed from timed-out'\
            f' by {mod_name}: <@{mod_id}> \n'
    if len(perms_removed) > 0:
        cdesc += 'Applied perms to: <'
        j = '>, <'
        if channel:
            cdesc += f'#'
            j += f'#'
        elif role:
            cdesc += f'@&'
            j += f'@&'
        elif category:
            cdesc += f'#'
            j += f'#'
        cdesc += f'{j}'.join(perms_removed)
        cdesc += '>'
    ccolour = Colours.COMMANDS
    return generic_embed(ctitle, cdesc, [], current_time(), ccolour)[0]


def timeout(user_name: str, user_id: str, mod_name: str, mod_id: str,
            channel: bool, role: bool, category: bool, perms_removed: list):
    """Timeout applied.

    Parameters
    ----------
    user_name: str
        name of the user
    user_id: str
        id of the user
    mod_name: str
        name of the mod
    mod_id: str
        id of the mod
    channel: bool
        if perms describe roles
    role: bool
        if perms describe channels
    category: bool
        if perms describe categories
    perms_removed: list
        list[id] of the target perms

    Returns
    -------
    discord.Embed
        embedded object to send message
    """
    ctitle = f'User Timed Out'
    cdesc = f'{user_name}: <@{user_id}> has been timed-out'\
            f' by {mod_name}: <@{mod_id}> \n'
    if len(perms_removed) > 0:
        cdesc += 'Removed perms to: <'
        j = '>, <'
        if channel:
            cdesc += f'#'
            j += f'#'
        elif role:
            cdesc += f'@&'
            j += f'@&'
        elif category:
            cdesc += f'#'
            j += f'#'
        cdesc += f'{j}'.join(perms_removed)
        cdesc += '>'
    ccolour = Colours.COMMANDS
    return generic_embed(ctitle, cdesc, [], current_time(), ccolour)[0]


"""
WARNINGS
"""


def warningeditembed(warn_name: str, warn_id: str, mod_name: str, mod_id: str,
                     major: bool, reason: str, warning_count: int):
    """Warning editted.

    Parameters
    ----------
    warn_name: str
        name of the user
    warn_id: str
        id of the user
    mod_name: str
        name of the mod
    mod_id: str
        id of the mod
    major: bool
        if major or minor
    reason: str
        reason for warn
    warning_count: int
        number of warnings for this user

    Returns
    -------
    discord.Embed
        embedded object to send message
    """
    level = 'MAJOR' if major else 'MINOR'
    ctitle = f'User Warning Edited'
    cdesc = f'{warn_name}: <@{warn_id}>'\
            f' has had a warning changed to **{level}** '\
            f'by {mod_name}: <@{mod_id}> for:\n'\
            f'\'**{reason}**\'.\n\n This is their '\
            f'{warning_count} warning.'
    ccolour = Colours.COMMANDS
    return generic_embed(ctitle, cdesc, [], current_time(), ccolour)[0]


def warningaddembed(warn_name: str, warn_id: str, mod_name: str, mod_id: str,
                    reason: str, major: bool, warning_count: int):
    """Warning added.

    Parameters
    ----------
    warn_name: str
        name of the user
    warn_id: str
        id of the user
    mod_name: str
        name of the mod
    mod_id: str
        id of the mod
    major: bool
        if major or minor
    reason: str
        reason for warn
    warning_count: int
        number of warnings for this user

    Returns
    -------
    discord.Embed
        embedded object to send message
    """
    level = 'MAJOR' if major else 'MINOR'
    ctitle = f'User Warned'
    cdesc = f'{warn_name}: <@{warn_id}>'\
            f' has been given a **{level}** warning '\
            f'by {mod_name}: <@{mod_id}> for:\n'\
            f'\'**{reason}**\'.\n\n This is their '\
            f'{warning_count} warning.'
    ccolour = Colours.COMMANDS
    return generic_embed(ctitle, cdesc, [], current_time(), ccolour)[0]


def warningrmembed(warn_name: str, warn_id: str, mod_name: str, mod_id: str,
                   warning_count: int):
    """Warning removed.

    Parameters
    ----------
    warn_name: str
        name of the user
    warn_id: str
        id of the user
    mod_name: str
        name of the mod
    mod_id: str
        id of the mod
    warning_count: int
        number of warnings for this user

    Returns
    -------
    discord.Embed
        embedded object to send message
    """
    ctitle = f'User Warning Forgiven'
    cdesc = f'{warn_name}: <@{warn_id}>'\
            f' has been forgiven for a warning '\
            f'by {mod_name}: <@{mod_id}>.\n\n This is their '\
            f'{warning_count} warning.'
    ccolour = Colours.COMMANDS
    return generic_embed(ctitle, cdesc, [], current_time(), ccolour)[0]


def warninglistembed(warn_name: str, warn_id: str, warned_user: discord.Member,
                     infractions: list, unshown: bool):
    """Warning list display.

    Parameters
    ----------
    warn_name: str
        name of the user
    warn_id: str
        id of the user
    warned_user: :func: discord.Member
        member object of the warned member, can be None if member not found
    infractions: list
        list[dict] of the warnings
    unshown: bool
        whether there are more warnings unshown

    Returns
    -------
    discord.Embed
        embedded object to send message
    """
    ctitle = f'Warning List'
    cdesc = f'{warn_name}: <@{warn_id}> warnings:'
    cdesc = f'' if infractions else f'User has no warnings.'
    ccolour = Colours.COMMANDS
    string_list = []
    for index, warning in enumerate(infractions):
        index = warning['id']
        level = 'MAJOR' if warning['major'] else 'MINOR'
        date = warning['logtime'].strftime('%b %d %Y %H:%M')
        tmp_warning_string = f'({level})'\
                             f' {warning["reason"]} '\
                             f'[{date}]\n'
        string_list.append([index, tmp_warning_string])

    if not isinstance(warned_user, type(None)):
        cdesc += f'\n**Join Date:** '\
                      f'{warned_user.joined_at.strftime("%b %d %Y %H:%M")}'

    if unshown:
        cdesc += f'\n\nThere are more warnings > 6 months ago.'

    return generic_embed(ctitle, cdesc, string_list,
                         current_time(), ccolour)[0]

"""
MODERATION
"""

def modlistembed(modded_name: str, modded_id: str, modded_user: discord.Member,
                     infractions: list, unshown: bool):
    """Warning list display.

    Parameters
    ----------
    modded_name: str
        name of the user
    modded_id: str
        id of the user
    modded_user: :func: discord.Member
        member object of the modded member, can be None if member not found
    infractions: list
        list[dict] of the infractions
    unshown: bool
        whether there are more infractions unshown

    Returns
    -------
    discord.Embed
        embedded object to send message
    """
    ctitle = f'Modaction List'
    cdesc = f'{modded_name}: <@{modded_id}> modactions:'
    cdesc = f'' if infractions else f'User has no modactions.'
    ccolour = Colours.COMMANDS
    string_list = []
    for index, moderation in enumerate(infractions):
        index = moderation['id']
        level = ModAction(moderation['action']).name
        date = moderation['logtime'].strftime('%b %d %Y %H:%M')
        tmp_string = f'({level})'\
                     f' {moderation["reason"]} '\
                     f'[{date}]\n'
        string_list.append([index, tmp_string])

    try:
        cdesc += f'\n**Join Date:** '\
                      f'{modded_user.joined_at.strftime("%b %d %Y %H:%M")}'
    except:
        pass
    if unshown:
        cdesc += f'\n\nThere are more modactions > 6 months ago.'

    return generic_embed(ctitle, cdesc, string_list,
                         current_time(), ccolour)[0]


def modeditembed(modded_name: str, modded_id: str, mod_name: str, mod_id: str,
                 action_type: ModAction, reason: str, infraction_count: int):
    """Modaction edit.

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
    infraction_count: int
        number of infractions for this user

    Returns
    -------
    discord.Embed
        embedded object to send message
    """
    ctitle = f'Modaction Editted'
    cdesc = f'{modded_name}: <@{modded_id}> modaction edited '\
            f'by {mod_name}: <@{mod_id}>'\
            f' previous modaction has been changed to a '\
            f'**{action_type.name}** action for:\n'\
            f'\'**{reason}**\'\n\n'\
            f'This is infraction number {infraction_count}'
    ccolour = Colours.COMMANDS
    return generic_embed(ctitle, cdesc, [], current_time(), ccolour)[0]


def modaddembed(modded_name: str, modded_id: str, mod_name: str, mod_id: str,
                action_type: ModAction, reason: str, infraction_count: int):
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
    infraction_count: int
        number of infractions for this user

    Returns
    -------
    discord.Embed
        embedded object to send message
    """
    ctitle = f'User Moderated'
    cdesc = f'{modded_name}: <@{modded_id}> was moderated ({action_type.name})'\
            f'by {mod_name}: <@{mod_id}> \n'\
            f'Reason: {reason}\n\n'\
            f'This is infraction number {infraction_count}'
    ccolour = Colours.CHANGE_G
    return generic_embed(ctitle, cdesc, [], current_time(), ccolour)[0]


def modrmembed(modded_name: str, modded_id: str, mod_name: str, mod_id: str,
               infraction_count: int):
    """Moderation removal.

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
    infraction_count: int
        number of infractions for this user

    Returns
    -------
    discord.Embed
        embedded object to send message
    """
    ctitle = f'User Modaction Removed'
    cdesc = f'{modded_name}: <@{modded_id}> had a modaction '\
            f'forgiven by {mod_name}: <@{mod_id}>\n\n'\
            f'They have {infraction_count} infractions.'
    ccolour = Colours.CHANGE_G
    return generic_embed(ctitle, cdesc, [], current_time(), ccolour)[0]

# end of code

# end of file
