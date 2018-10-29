# -*- coding:utf-8 -*-
import hashlib
import json


class Block:
    """
    区块类
    """

    def __init__(self, index, timestamp, data, previous_hash=' '):
        """
        初始化函数
        """
        self.index         = index
        self.timestamp     = timestamp
        self.data          = data
        self.previous_hash = previous_hash
        self.hash          = self.calculate_hash()

    def calculate_hash(self):
        """
        计算hash
        """
        return hashlib.sha256(str(self.index) + self.previous_hash + self.timestamp + json.dumps(self.data)).hexdigest()

    def print_block(self):
        """
        输出区块信息
        """
        print "Block #" + str(self.index)
        print "Data " + str(self.data)
        print "Block Hash: " + str(self.hash)
        print "Block Previous: " + str(self.previous_hash)


class BlockChain:
    """
    区块链类
    """

    def __init__(self):
        """
        初始化函数
        """
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        """
        创建创世块
        """
        return Block(0, "29/10/2018", "Genesis Block", "0")

    def get_last_block(self):
        """
        获取最近的一个区块
        """
        return self.chain[len(self.chain) - 1]

    def add_block(self, new_block):
        """
        添加区块
        """
        new_block.previous_hash = self.get_last_block().hash
        new_block.hash          = new_block.calculate_hash()
        self.chain.append(new_block)

    def is_chain_valid(self):
        """
        校验区块链是否合法
        """
        chain_len = len(self.chain)
        for i in range(1, chain_len):
            current_block  = self.chain[i]
            previous_block = self.chain[i-1]
            # 校验数据是否被篡改
            if current_block.hash != current_block.calculate_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
        return True

    def print_block_chain(self):
        """
        输出区块链
        """
        chain_len = len(self.chain)
        for i in range(1, chain_len):
            self.chain[i].print_block() 

if __name__ == "__main__":
    my_coin = BlockChain()
    my_coin.add_block(Block(1, "23/10/2018", {"account": "DoubleQ", "amount": 25, "action": "buy"}))
    my_coin.add_block(Block(2, "24/10/2018", {"account": "Eric", "amount": 10, "action": "buy"}))
    my_coin.add_block(Block(3, "25/10/2018", {"account": "Winky", "amount": 20, "action": "buy"}))
    my_coin.add_block(Block(4, "26/10/2018", {"account": "Xxz", "amount": 4, "action": "buy"}))
    my_coin.print_block_chain()
    print "Chain valid? " + str(my_coin.is_chain_valid())
    my_coin.chain[1].data = {"account": "DoubleQ", "amount": 100, "action": "buy"}
    print "Chain valid? " + str(my_coin.is_chain_valid())