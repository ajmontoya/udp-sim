import dgram from 'node:dgram';
import { exit } from 'node:process';

const server = dgram.createSocket('udp4');

server.on('error', (err) => {
    console.log(`Server error:\n${err.stack}`);
    server.close();
});

server.on('message', (msg, rinfo) => {
    console.log(`Server got: ${msg} from ${rinfo.address}:${rinfo.port}`);
});

server.on('listening', () => {
    const address = server.address();
    console.log(`Server listening ${address.address}:${address.port}`);
});

server.bind(41234);

process.on('SIGINT', () => {
    console.log('Exiting...');
    server.close();
    exit(0);
});
