package io.ph.bot.commands.general;

import java.awt.Color;
import java.util.Date;
import java.text.SimpleDateFormat;
import java.lang.Long;
import java.time.OffsetDateTime;

import io.ph.bot.commands.Command;
import io.ph.bot.commands.CommandCategory;
import io.ph.bot.commands.CommandData;
import io.ph.bot.model.Permission;
import io.ph.util.MessageUtils;
import io.ph.util.Util;
import net.dv8tion.jda.api.EmbedBuilder;
import net.dv8tion.jda.api.entities.Message;
import net.dv8tion.jda.api.utils.MiscUtil;
import net.dv8tion.jda.api.utils.TimeUtil;

/**
 * Special Snowflake converter
 * @author Nick
 *
 */
@CommandData (
        defaultSyntax = "snowflaketime",
        aliases = {"convertid", "id"},
        category = CommandCategory.UTILITY,
        permission = Permission.NONE,
        description = "Converts a given snowflake ID to a time in UTC",
        example = "149945199873884160 # converts to "
        )
public class SnowflakeTime extends Command {

    @Override
    public void executeCommand(Message msg) {
        EmbedBuilder em = new EmbedBuilder();
        String contents = Util.getCommandContents(msg);

        if(contents.isEmpty()) {
            MessageUtils.sendIncorrectCommandUsage(msg, this);
            return;
        }

        if(Util.isInteger(contents)) {
            Long snow = Long.parseLong(contents);
            OffsetDateTime date = TimeUtil.getTimeCreated(snow);
            // the format of your date
            String formattedDate = TimeUtil.getDateTimeString(date);
            em.setColor(Color.GREEN)
            .setTitle("Converted " + contents + " to " + formattedDate, null);
        } else {
            MessageUtils.sendIncorrectCommandUsage(msg, this);
            return;
        }
        msg.getChannel().sendMessage(em.build()).queue();
    }

}
