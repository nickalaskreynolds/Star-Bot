"""General Embed Dialog Hub."""

# internal modules

# external modules
import discord
import asyncio
from discord.ext import commands

# relative modules
from .colours import Colours
from .embed_general import generic_embed

# global attributes
__all__ = ('iterator',
           'confirm')
__filename__ = __file__.split('/')[-1].strip('.py')
__path__ = __file__.strip('.py').strip(__filename__)


async def iterator(ctx: commands.Context, step: dict, timeout: int):
    """Generic iterator embedder.

    Will ask a series of questions and save the results

    Parameters
    ----------
    ctx: :func: commands.Context
        the context command object
    step: dict
        dictionary of key='question to display', value=blank (to be populated)
    timeout: int
        the timeout in seconds before cancel for any subcommand

    Returns
    -------
    dict
        the same dictionary with value overriden
    """
    message = generic_embed(f'Please answer these questions ({timeout}s timer):', '', [], Colours.DIALOG_T)
    request = await ctx.send(embed=message)
    failed = False

    for question in step.keys():
        tmp_r = await ctx.send(f'{question}')
        try:
            tmp_m = await ctx.bot.wait_for("message",
                                           timeout=timeout,
                                           check=lambda message:
                                           message.author == ctx.message.author)
            step[question] = tmp_m.clean_content
        except asyncio.TimeoutError:            
            failed = True
        except Exception as e:
            print(f'Error in reacting to message: {e}')
        try:
            await tmp_r.delete()
            await tmp_m.delete()
        except Exception as e:
            print(f'Error in deleting message: {e}')
        if failed:
            break

    try:
        await request.delete()
        if not failed:
            await ctx.message.add_reaction(r'✅')
        else:
            ctx.message.add_reaction(r'❌')
            return False
    except Exception as e:
        print(f'Error in deleting/reacting to message: {e}')
    return step


async def confirm(ctx: commands.Context, message: str, timeout: int):
    """Generic confirmation embedder.

    Serves as a confirm/deny embed builder with a Xs timeout

    Parameters
    ----------
    ctx: :func: commands.Context
        the context command object
    message: str
        the message to display
    timeout: int
        the timeout in seconds before cancel

    Returns
    -------
    bool
        success true false
    """
    confirmdialog = f'\nAttempting to {ctx.command}:\n'\
                    f'{message}'\
                    f'\n➡️ Type `confirm` to {ctx.command}'\
                    ' or literally anything else to cancel.'\
                    f'\n\n*You have {timeout}s...*'
    message = generic_embed(r'❗ Confirmation Request ❗', confirmdialog, [], Colours.DIALOG_T)
    request = await ctx.send(embed=message, delete_after=timeout)
    try:
        message = await ctx.bot.wait_for("message",
                                         timeout=timeout,
                                         check=lambda message:
                                         message.author == ctx.message.author)
    except asyncio.TimeoutError:
        ctx.message.add_reaction(r'❌')
        return False
    if message.clean_content.lower() != 'confirm':
        ctx.message.add_reaction(r'❌')
        return False
    try:
        await request.delete()
        await message.delete()
        await ctx.message.add_reaction(r'✅')
    except Exception as e:
        print(f'Error in deleting message: {e}')
    return True

# end of code

# end of file
