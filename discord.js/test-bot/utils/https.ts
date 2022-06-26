// use this module with the following line of code:
// require('./utils/https');  ---  typescript specific

import express from 'express';

const port: number = 3000;
const app: express.Application = express();

app.get('/', (req, res) => res.send('Bot is ON!'));
app.listen(port, () => console.log(`Running on ${port}!`));
