import hashlib
import time

class Block:
    def __init__(self, index, transactions, timestamp, previous_hash):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = 0  # Used for mining
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = "{}{}{}{}{}".format(self.index, self.transactions, self.timestamp, self.previous_hash, self.nonce)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self, difficulty):
        # Mining by trying different nonce values
        target = '0' * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        print("Block mined: ", self.hash)

class Blockchain:
    def __init__(self, difficulty=2):
        self.chain = [self.create_genesis_block()]
        self.difficulty = difficulty
        self.pending_transactions = []
        self.mining_reward = 10

    def create_genesis_block(self):
        return Block(0, "Genesis Block", time.time(), "0")

    def get_last_block(self):
        return self.chain[-1]

    def add_block(self, block):
        block.previous_hash = self.get_last_block().hash
        block.mine_block(self.difficulty)
        self.chain.append(block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            if current.hash != current.calculate_hash():
                print("Current Hashes not equal")
                return False

            if current.previous_hash != previous.hash:
                print("Previous Hashes not equal")
                return False

        return True

# Example usage
if __name__ == "__main__":
    myBlockchain = Blockchain()
    myBlockchain.add_block(Block(1, "First Block", time.time(), myBlockchain.get_last_block().hash))
    myBlockchain.add_block(Block(2, "Second Block", time.time(), myBlockchain.get_last_block().hash))

    for block in myBlockchain.chain:
        print(f"Block #{block.index} [{block.hash}]")

    print("Blockchain valid?", myBlockchain.is_chain_valid())
