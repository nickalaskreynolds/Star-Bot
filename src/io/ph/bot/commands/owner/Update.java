package io.ph.bot.commands.owner;

import io.ph.bot.commands.Command;
import io.ph.bot.commands.CommandCategory;
import io.ph.bot.commands.CommandData;
import io.ph.bot.jobs.StatusChangeJob;
import io.ph.bot.model.Permission;
import io.ph.util.Util;
import io.ph.bot.Bot;
import net.dv8tion.jda.api.entities.Message;
import net.dv8tion.jda.api.EmbedBuilder;
import java.awt.Color;
import java.util.List;

/**
 * Command to send an update message to current guild and all guild owners
 * @author Nick
 */

@CommandData (
        defaultSyntax = "update",
        aliases = {},
        category = CommandCategory.BOT_OWNER,
        permission = Permission.BOT_OWNER,
        description = "Start an update timer in the status to say \"Restart in n\" where n is minutes."
                + " Doesn't actually kill the bot at 0",
        example = "5"
        )
public class Update extends Command {

    @Override
    public void executeCommand(Message msg) {
        EmbedBuilder em = new EmbedBuilder();
        try {
            StatusChangeJob.commenceUpdateCountdown(Integer.parseInt(Util.getCommandContents(msg)));
            msg.getChannel().sendMessage("Updating in " + Util.getCommandContents(msg) + " minutes.").queue(success -> {msg.delete().queue();});
        } catch(NumberFormatException e) {
            msg.getChannel().sendMessage(Util.getCommandContents(msg) + " is not a valid integer");
        }
    }
}
