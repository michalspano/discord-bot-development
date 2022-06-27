import { MessageEmbed } from 'discord.js';

// we try to simulate a `struct` (similar to C) to store the date
export const TIME: { [key: string]: number } = {
    'year': Number(), 'month': Number(), 'day': Number()
}
export const ERROR: string = '🆘';
export const OK_EMOJI: string = '🆗';
const EMBED_URL: string = 'https://lh4.googleusercontent.com/go80mh9N90WT7n0mIZM5Kl9uuZhLYLHz-wmPnnx3ioTH2MBivRSLpCKsWoMGWBcgGpo=w2400';

export const getDaysSince: Function = (start: { [key: string]: number }): number => {
    const initialDate: Date = new Date(start.year, start.month - 1, start.day);
    const maxDays: number = new Date(start.year, start.month, 0).getDate();     // here we validate the max. number of days in the month
    if (start.day > maxDays) return -1;                                         // compare the day with the max. number of days in the month
    return Math.floor((Date.now() - initialDate.getTime()) / (1000 * 3600 * 24));
}
export const embedUsage: Function = (botID: number): MessageEmbed => {
    return new MessageEmbed()
        .setTitle('⏰ | Days Since ')
        .setFields([
            { name: "I'll count days since ...", value: `<@${botID}> **count** \`DD:MM:YY\`` }
        ])
        .setColor('#ffaa00')
        .setImage(EMBED_URL)
}
export const embedDaysSince = (dayCount: number, dayStart: string): MessageEmbed => {
    return new MessageEmbed()
        .setTitle(`Days Since \`${dayStart}\``)
        .setColor('#ffaa00')
        .setFields([
            { name: '**Count**', value: `${dayCount}` }
        ])
        .setImage(EMBED_URL)
}