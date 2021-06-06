import hashlib
class Block:
    def __init__(self, index, timestamp, content, previous_hash):
      self.index = index
      self.timestamp = timestamp
      self.content = content
      self.previous_hash = previous_hash
      self.hash = self.calc_hash()

    def calc_hash(self):
      sha = hashlib.sha256()
      sha.update(str(self.index).encode('utf-8') +
                 str(self.timestamp).encode('utf-8') +
                 str(self.content).encode('utf-8') +
                 str(self.previous_hash).encode('utf-8'))
      return sha.hexdigest()

M4BlockChain = []

from datetime import datetime
def create_genesis_block():
    return Block(0, datetime.now(), "Genesis Block", "0")

M4BlockChain.append(create_genesis_block())


# write a function `next_block` to generate a block
def next_block(last_block):
  i = last_block.index + 1
  hash = last_block.calc_hash()
  block = Block(i, datetime.now(), "this is block {}".format(i), hash)
  return block

# append 5 blocks to the blockchain
def app_five(block_list):
  for _ in range(5):
    last_block = block_list[-1]
    block = next_block(last_block)
    block_list.append(block)
  return block_list


# block_list = app_five(M4BlockChain)

# block2 = block_list[2]
# block3 = block_list[3]
# print(block2.calc_hash())
# print(block3.previous_hash)
