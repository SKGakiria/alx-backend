// Script to connect Redis server
import { createClient } from 'redis';
import { promisify } from 'util';

const client = createClient();

client.on('connect', async () => {
  console.log('Redis client connected to the server');
  await main();
});

client.on('error', (err) => {
  console.error(`Redis client not connected to the server: ${err.message}`);
});

const setNewSchool = async (schoolName, value) => {
  client.set(schoolName, value, (err, reply) => {
    console.log(reply);
  });
};

const displaySchoolValue = async (schoolName) => {
  console.log(await promisify(client.get).bind(client)(schoolName));
};

async function main() {
  await displaySchoolValue('Holberton');
  setNewSchool('HolbertonSanFrancisco', '100');
  await displaySchoolValue('HolbertonSanFrancisco');
}
