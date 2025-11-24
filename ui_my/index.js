require('http').createServer((req, res) => {
  res.end('OK');
}).listen(3000, () => console.log('Running on :3000'));

