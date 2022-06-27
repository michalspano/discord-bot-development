#!/usr/bin/env ts-node
import dotenv from 'dotenv';
import DiscordJS, { Intents } from 'discord.js';
import { TIME, ERROR, OK_EMOJI } from './utils/utils';
import { getDaysSince, embedUsage, embedDaysSince } from './utils/utils';

dotenv.config();            // instantiate the dotenv variables
require('./utils/https')    // instantiate the HTTPS monitor

const client: DiscordJS.Client = new DiscordJS.Client({
    intents: [
        Intents.FLAGS.GUILDS,
        Intents.FLAGS.GUILD_MESSAGES,
        Intents.FLAGS.GUILD_MESSAGE_REACTIONS
    ]
});

client.on('ready', (): void => {
    console.log(`${client.user!.tag} is online!`)
    client.user!.setActivity('Counting Days...');
});

client.on('messageCreate', async (msg: DiscordJS.Message): Promise<void> => {
    if (msg.author.bot) return; // don't reply to bots - base case
    
    if (msg.mentions.has(client.user!.id)) {
        const command: string = msg.content.trim().split(' ')[1];

        if (!command) {  // show the usage if no command is provided
            await msg.react(OK_EMOJI); 
            await msg.channel.send({ embeds: [embedUsage(client.user!.id)] });

        } else {
            const args: string[] = msg.content.trim().split(' ').slice(2)
                .filter((arg: string) => arg != '');

            if (command === 'count') {
                if (args.length == 1) {
                    msg.react(OK_EMOJI); // react that the command is being processed

                    const [day, month, year]: string[] = args[0].split(':');
                    TIME.year = Number(year); TIME.month = Number(month); TIME.day = Number(day);

                    // detect if any is NaN => invalid date (error)
                    if ((Object.keys(TIME).map(key => TIME[key]).filter(val => isNaN(val))).length) {
                        await msg.react(ERROR); await msg.reactions.resolve(OK_EMOJI)?.remove();
                        return;
                    }
                    const dayCount: number = getDaysSince(TIME);

                    // we don't permit negative number of days
                    if (dayCount < 0) { 
                        await msg.react(ERROR); await msg.reactions.resolve(OK_EMOJI)?.remove();
                        return; 
                    }
                    // embed the final result, indicating that no error was found   
                    const dayStartFormat: string = args[0].split(';').join(' ');
                    await msg.channel.send({ embeds: [embedDaysSince(dayCount, dayStartFormat)] });

                } else {
                    // error, too many arguments; explain the usage
                    await msg.react(ERROR);
                    await msg.channel.send({ embeds: [embedUsage(client.user!.id)] });
                }
            } 
        }
    }
});

client.login(process.env.TOKEN);