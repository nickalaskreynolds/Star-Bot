package io.ph.bot;

import java.io.File;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;

import javax.security.auth.login.LoginException;

import org.apache.commons.configuration.Configuration;
import org.apache.commons.configuration.PropertiesConfiguration;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import io.ph.bot.events.CustomEventDispatcher;
import io.ph.bot.exception.NoAPIKeyException;
import io.ph.bot.feed.TwitterEventListener;
import io.ph.bot.jobs.StatusChangeJob;
import io.ph.bot.listeners.Listeners;
import io.ph.bot.listeners.ModerationListeners;
import io.ph.bot.listeners.VoiceChannelListeners;
import io.ph.bot.scheduler.JobScheduler;
import io.ph.util.MessageUtils;
import java.util.concurrent.atomic.AtomicInteger;
import io.ph.bot.ws.WebsocketServer;
import net.dv8tion.jda.api.AccountType;
import net.dv8tion.jda.api.JDA;
import net.dv8tion.jda.api.JDABuilder;
import net.dv8tion.jda.api.OnlineStatus;
import net.dv8tion.jda.api.entities.Activity;
import net.dv8tion.jda.api.entities.Guild;
import net.dv8tion.jda.api.entities.TextChannel;
import net.dv8tion.jda.api.entities.User;
import net.dv8tion.jda.api.entities.VoiceChannel;
import net.dv8tion.jda.api.exceptions.RateLimitedException;

/**
 * Singleton instance of the entire bot. Includes configuration and the main JDA singleton
 * @author Nick
 *
 */
public class Bot {
    private static final Bot instance;
    public Shards shards;
    private static ArrayList<JDA> jdaClients;
    private final static Logger logger = LoggerFactory.getLogger(Bot.class);

    // Sharding splits the connection gateways to Discord and splits servers
    // among the shards. Discord limits you to 2500 guilds per shard, so you should
    // try and make it so TOTAL_GUILDS/SHARD_COUNT ~= 1750
    // TODO: Move this to configuration
    private final static int SHARD_COUNT = 1;

    // Set to true if you want various debug statements
    public static final boolean DEBUG = false;
    public static final String BOT_VERSION = "1.0.1.1";
    public static final String REPO = "<https://github.com/nickalaskreynolds/Star-Bot>";
    public static boolean isReady = false;

    private APIKeys apiKeys = new APIKeys();
    private BotConfiguration botConfig = new BotConfiguration();
    private CustomEventDispatcher eventDispatcher = new CustomEventDispatcher();

    public void start(String[] args) throws LoginException, IllegalArgumentException, InterruptedException, RateLimitedException {
        if (!loadProperties()) {
            logger.error("Could not load Bot.properties correctly."
                    + " Make sure every field is filled, including MaxSongLength");
            System.exit(1);
        }
        jdaClients = new ArrayList<>(SHARD_COUNT);
        if (SHARD_COUNT > 1) {
            for (int i = 0; i < SHARD_COUNT; i++) {
                jdaClients.add(new JDABuilder(AccountType.BOT)
                        .setToken(botConfig.getToken())
                        .setStatus(OnlineStatus.DO_NOT_DISTURB)
                        .setActivity(Activity.playing("launching..."))
                        .addEventListeners(new Listeners(), new ModerationListeners(), new VoiceChannelListeners())
                        .useSharding(i, SHARD_COUNT)
                        .build());
            }
        } else {
            jdaClients.add(new JDABuilder(AccountType.BOT)
                    .setToken(botConfig.getToken())
                    .setStatus(OnlineStatus.DO_NOT_DISTURB)
                    .setActivity(Activity.playing("launching..."))
                    .addEventListeners(new Listeners(), new ModerationListeners(), new VoiceChannelListeners())
                    .build());
        }
        shards = new Shards();
        State.changeBotPresence(OnlineStatus.ONLINE);
        initialize();
        isReady = true;

        String botdevID = Long.toString(Bot.getInstance().getConfig().getbotDeveloperId());
        AtomicInteger guildNum = new AtomicInteger(0);

        Bot.getInstance().getBots().forEach(j -> {
            j.getGuilds().forEach(g -> {
                guildNum.incrementAndGet();
            });
        });

        String logMsg = "Bot is now logged on in: " + guildNum.toString() + " guilds";
        MessageUtils.sendPrivateMessage(botdevID, logMsg);
    }

    /**
     * Bot initialization after ready state returns
     */
    private static void initialize() {
        JobScheduler.initializeScheduler();
        TwitterEventListener.initTwitter();
        WebsocketServer.getInstance().start();
    }

    public boolean loadProperties() {
        try {
            PropertiesConfiguration config = new PropertiesConfiguration("resources/Bot.properties");
            botConfig.setToken(config.getString("BotToken"));
            botConfig.setAvatar(config.getString("Avatar"));
            botConfig.setBotOwnerId(config.getLong("BotOwnerId", 0));
            botConfig.setbotDeveloperId(config.getLong("BotDeveloperId", 0));
            botConfig.setBotInviteLink(config.getString("InviteLink"));
            botConfig.setBotInviteBotLink(config.getString("InviteBotLink"));
            botConfig.setMaxSongLength(config.getInt("MaxSongLength", 15));
            botConfig.setCompanionBot(config.getBoolean("MusicCompanion", false));

            Configuration subset = config.subset("apikey");
            Iterator<String> iter = subset.getKeys();
            while(iter.hasNext()) {
                String key = iter.next();
                String val = subset.getString(key);
                if(val.length() > 0) {
                    this.apiKeys.put(key, val);
                    logger.info("Added API key for: {}", key);
                }
            }
            StatusChangeJob.setStatuses(config.getStringArray("StatusRotation"));
            return true;
        } catch (Exception e) {
            e.printStackTrace();
            return false;
        }
    }

    static {
        instance = new Bot();
    }    

    public static Bot getInstance() {
        return instance;
    }

    public ArrayList<JDA> getBots() {
        return jdaClients;
    }

    public APIKeys getApiKeys() {
        return this.apiKeys;
    }

    public BotConfiguration getConfig() {
        return this.botConfig;
    }

    public CustomEventDispatcher getEventDispatcher() {
        return eventDispatcher;
    }

    public class APIKeys {
        private Map<String, String> keys = new HashMap<String, String>();

        /**
         * Get API key for given key
         * @param key Key to get
         * @return String of value, null if not found
         */
        public String get(String key) throws NoAPIKeyException {
            if (keys.get(key) == null)
                throw new NoAPIKeyException();
            return keys.get(key);
        }

        void put(String key, String val) {
            this.keys.put(key, val);
        }
    }

    public class BotConfiguration {
        private String token, avatar, botInviteLink, botInviteBotLink;
        private boolean companionBot;
        private long botOwnerId;
        private long botDeveloperId;
        private int maxSongLength; // in minutes

        public boolean isCompanionBot() {
            return this.companionBot;
        }

        public void setCompanionBot(boolean companionBot) {
            this.companionBot = companionBot;
        }

        public int getMaxSongLength() {
            return maxSongLength;
        }

        public void setMaxSongLength(int songLength) {
            this.maxSongLength = songLength;
        }

        public String getToken() {
            return token;
        }

        public void setToken(String token) {
            this.token = token;
        }

        public long getBotOwnerId() {
            return botOwnerId;
        }

        public void setBotOwnerId(long botOwnerId) {
            this.botOwnerId = botOwnerId;
        }

        public String getAvatar() {
            return avatar;
        }

        public void setAvatar(String avatar) {
            this.avatar = avatar;
        }

        public String getBotInviteLink() {
            return botInviteLink;
        }

        public void setBotInviteLink(String botInviteLink) {
            this.botInviteLink = botInviteLink;
        }

        public String getBotInviteBotLink() {
            return botInviteBotLink;
        }

        public void setBotInviteBotLink(String botInviteBotLink) {
            this.botInviteBotLink = botInviteBotLink;
        }

        public long getbotDeveloperId() {
            return botDeveloperId;
        }

        public void setbotDeveloperId(long botDeveloperId) {
            this.botDeveloperId = botDeveloperId;
        }
    }

    public class Shards {
        /**
         * Get a guild from an ID from all shards
         * @param guildId Guild ID
         * @return Guild if found, null if not
         */
        public Guild getGuildById(long guildId) {
            for (JDA j : jdaClients) {
                Guild g;
                if ((g = j.getGuildById(guildId)) != null) {
                    return g;
                }
            }
            return null;
        }

        public Guild getGuildById(String guildId) {
            try {
                return getGuildById(Long.parseLong(guildId));
            } catch (NumberFormatException e) {
                return null;
            }
        }

        /**
         * Get a text channel from an ID from all shards
         * @param channelId Channel ID
         * @return TextChannel if found, null if not
         */
        public TextChannel getTextChannelById(long channelId) {
            for (JDA j : jdaClients) {
                TextChannel t;
                if ((t = j.getTextChannelById(channelId)) != null) {
                    return t;
                }
            }
            return null;
        }

        public TextChannel getTextChannelById(String channelId) {
            try {
                return getTextChannelById(Long.parseLong(channelId));
            } catch (NumberFormatException e) {
                return null;
            }
        }

        /**
         * Get a voice channel from an ID from all shards
         * @param channelId Channel ID
         * @return VoiceChannel if found, null if not
         */
        public VoiceChannel getVoiceChannelById(long channelId) {
            for (JDA j : jdaClients) {
                VoiceChannel c;
                if ((c = j.getVoiceChannelById(channelId)) != null) {
                    return c;
                }
            }
            return null;
        }

        public VoiceChannel getVoiceChannelById(String channelId) {
            try {
                return getVoiceChannelById(Long.parseLong(channelId));
            } catch (NumberFormatException e) {
                return null;
            }
        }

        /**
         * Get a user from an ID from all shards
         * @param userId User ID
         * @return User if found, null if not
         */
        public User getUserById(long userId) {
            for (JDA j : jdaClients) {
                User u = j.getUserById(userId);
                if (u != null) {
                    String s = String.valueOf(userId);
                    System.out.println(s);
                    return u;
                }
            }
            return null;
        }

        public User getUserById(String userId) {
            try {
                return getUserById(Long.parseLong(userId));
            } catch (NumberFormatException e) {
                return null;
            }
        }
    }
}
