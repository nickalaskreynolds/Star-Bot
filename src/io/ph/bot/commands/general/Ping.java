package io.ph.bot.commands.general;

import java.awt.Color;

import io.ph.bot.commands.Command;
import io.ph.bot.commands.CommandCategory;
import io.ph.bot.commands.CommandData;
import io.ph.bot.model.Permission;
import io.ph.util.Util;
import io.ph.util.MessageUtils;
import net.dv8tion.jda.api.EmbedBuilder;
import net.dv8tion.jda.api.entities.Message;

@CommandData (
        defaultSyntax = "ping",
        aliases = {"ping"},
        category = CommandCategory.UTILITY,
        permission = Permission.NONE,
        description = "HELLO? Am I alive?",
        example = ""
        )
public class Ping extends Command {
    @Override
    public void executeCommand(Message msg) {
        EmbedBuilder em = new EmbedBuilder();
        em.setTitle("Ping?", null)
        .setDescription("Pong!")
        .setFooter(msg.getJDA().getGatewayPing() + "ms", null)
        .setColor(Util.resolveColor(Util.memberFromMessage(msg), Color.MAGENTA));
        MessageUtils.sendMessage(msg.getChannel().getId(),em.build(),5);
        msg.delete().queue();
    }
}
