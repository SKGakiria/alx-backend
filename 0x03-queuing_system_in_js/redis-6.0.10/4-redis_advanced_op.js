// Use of client to store a hash value
import { createClient, print } from 'redis';

const client = createClient();

client.on('connect', () => {
  console.log('Redis client connected to the server');
  main();
});

client.on('error', (err) => {
  console.error(`Redis client not connected to the server: ${err.message}`);
});

const updateHash = (hashName, fieldName, fieldValue) => {
  client.hset(hashName, fieldName, fieldValue, print);
};

const printHash = (hashName) => {
  client.hgetall(hashName, (err, reply) => { 
    console.log(reply);
  });
};

function main() {
  const hashObj = {
    Portland: 50,
    Seattle: 80,
    'New York': 20,
    Bogota: 20,
    Cali: 40,
    Paris: 2,
  };
  for (const [field, val] of Object.entries(hashObj)) {
    updateHash('HolbertonSchools', field, val);
  }
  printHash('HolbertonSchools');
}
