const Web3 = require('web3')
const fs = require('fs');

const key1 = `44c73b7008dd487699cf142341c3be80`
const key2 = `1389e883f22c438fa448e9bdb1a5dd62`
const key3 = `fd9e83bd951b44ca804fa849c5860cf8`

const web3 = new Web3(new Web3.providers.HttpProvider(`https://mainnet.infura.io/v3/${key1}`))

var args          = process.argv.slice(2);
// let latest        = 13516239
let latest        = 13515990
let num_blocks    = args[0]

const writeStream = fs.createWriteStream(`../../data/${num_blocks}_large_addresses_from_${latest}.txt`);
const pathName    = writeStream.path;

let run = async () => {
  let addresses = {}

  while (true) {
    // update the number of blocks left 
    let blocks_left = num_blocks--
    if (!blocks_left)
      break

    // update the current block number to explore
    let block_num = latest--
    let block = await web3.eth.getBlock(block_num)
    if (!block)
      break

    console.log('block', block_num, 'transactions', block.transactions.length, 'blocks left', blocks_left)
    for(let i = 0; i < block.transactions.length; i++) {
      let tx = await web3.eth.getTransaction(block.transactions[i])

      // tx value should be non-zero
      let tx_val = parseInt(tx.value) * Math.pow(10,-18)
      if (0.01 <= tx_val && tx_val <= 2) {
        if (tx.to !== null)
          addresses[tx.to]   = true
        
        if (tx.from !== null)
          addresses[tx.from] = true
      }
    }
  }

  let large_addresses = []
  for (address in addresses) {
    try {
      let balance = await web3.eth.getBalance(address)

      // eth balance should be between 1 and 10
      let eth_bal = balance * Math.pow(10,-18)
      if (1 <= eth_bal && eth_bal <= 10) {
        large_addresses.push(address)
      }
    } catch (err) {
      console.log(err)
    }
  }
  // write each value of the array on the file breaking line
  large_addresses.forEach(value => writeStream.write(`${value}\n`));

  // the finish event is emitted when all data has been flushed from the stream
  writeStream.on('finish', () => {
    console.log(`>>> done. wrote data to the file ${pathName}`);
  });

  // handle the errors on the write process
  writeStream.on('error', (err) => {
      console.error(`>>> there was an error writing to the file ${pathName} => ${err}`)
  });

  // close the stream
  writeStream.end();
}

run()