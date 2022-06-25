// ================ HTTPS MONITOR ================
import express from 'express';

const app = express();
const port: Number = 3000;

app.get('/', (req, res) => res.send('Bot is ON!'));
app.listen(port, () => console.log(`Running on ${port}!`));

// ================ BOT CODE ================

import dotenv from 'dotenv';
import DiscordJS, { Intents } from 'discord.js';

dotenv.config();

const client = new DiscordJS.Client({
    intents: [
        Intents.FLAGS.GUILDS,
        Intents.FLAGS.GUILD_MESSAGES,
        Intents.FLAGS.GUILD_MESSAGE_REACTIONS 
    ]
});

client.on('ready', (): void => {
    console.log(`${client.user!.tag} is online!`);
});

client.on('messageCreate', async (msg): Promise<void> => {
    if (msg.author.bot) return; // don't reply to bots

    if (msg.content === 'ping') { 
        await msg.reply('pong'); await msg.react('🤖');
    }
});

client.login(process.env.TOKEN);