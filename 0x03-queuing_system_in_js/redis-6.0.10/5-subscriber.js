// Create a redis client for the subscriber
import { createClient } from 'redis';

const client = createClient();
const EXIT_MSG = 'KILL_SERVER';

client.on('connect', () => {
  console.log('Redis client connected to the server');
  client.subscribe('holberton school channel');
});

client.on('error', (err) => {
  console.error(`Redis client not connected to the server: ${err.message}`);
});

client.on('message', (chan, msg) => {
  console.log(msg);
  if (msg === EXIT_MSG) {
    client.unsubscribe();
    client.quit();
  }
});
