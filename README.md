<h1>区块内容</h1>

通常，一个区块包含数据、时间戳、指向上一个区块的索引。今天的简易区块类Block主要包含以下几个属性：

<ul>
<li>index：链上用来追踪区块位置的编号</li>
<li>timestamp：区块创建的时间或日期</li>
<li>data：真实存储在区块上的数据</li>
<li>previous hash：链上上一个区块的hash码</li>
</ul>

使用SHA-256算法计算区块的hash码

<pre><code class="language-python line-numbers">class Block:
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
</code></pre>

<h1>区块链</h1>

<h2>初始化一条链</h2>

首先链上的第一个区块被称作"创世块"，这个区块仅作为整条链的始端。在本次实现中，当BlockChain实例化后，便自动创建创世块。

<h2>添加一个区块</h2>

为了向链上添加一个区块，需要先获取链上最后一个区块的hash码，然后计算新区块的hash码。get_last_block方法用来获取链的最后一个区块，当做添加新区块操作时，原来链上的最后一个区块就变成了上一个区块（相对于新区块来说）。

<h2>链的安全性</h2>

链在设计上防止被修改。确保链安全性的一部分是保证两个相邻区块不会被修改，例如区块#3的previous_hash码需要严格等于#2的hash码，本次实现中通过is_chain_valid方法进行校验。另一部分是确保块创建后数据不会被修改，如果数据更改，块本身对应hash码也会被修改（因为data是计算hash码的元素之一），hash码值的变更将被is_chain_valid方法校验出来。

<pre><code class="language-python line-numbers">class BlockChain:
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
</code></pre>

<h1>测试区块链</h1>

测试上面写好的程序，创建一个名叫my_coin的BlockChain实例，并且向链上添加区块。通过is_chain_valid方法校验链的合法性，并试图改变某个区块的值，看是否能通过合法性校验。

<pre><code class="language-python line-numbers">if __name__ == "__main__":
    my_coin = BlockChain()
    my_coin.add_block(Block(1, "23/10/2018", {"account": "DoubleQ", "amount": 25, "action": "buy"}))
    my_coin.add_block(Block(2, "24/10/2018", {"account": "Eric", "amount": 10, "action": "buy"}))
    my_coin.add_block(Block(3, "25/10/2018", {"account": "Winky", "amount": 20, "action": "buy"}))
    my_coin.add_block(Block(4, "26/10/2018", {"account": "Xxz", "amount": 4, "action": "buy"}))
    my_coin.print_block_chain()
    print "Chain valid? " + str(my_coin.is_chain_valid())
    my_coin.chain[1].data = {"account": "DoubleQ", "amount": 100, "action": "buy"}
    print "Chain valid? " + str(my_coin.is_chain_valid())
</code></pre>

输出如下：

<pre><code class="language-shell line-numbers">Block #1
Data {'action': 'buy', 'account': 'DoubleQ', 'amount': 25}
Block Hash: 20d59499ef38bda24de15df140fd195b2627a9707453c6afd12458866ab5eba9
Block Previous: c3f4fe865ecc110ea0ed13fb3602beb2468eb2fdedc7a9aeb9eec245dd414763
Block #2
Data {'action': 'buy', 'account': 'Eric', 'amount': 10}
Block Hash: 0797ecc35e15f4758b635ee4053006bbb9a61ca9cba8876fbfa6d9a2c186a882
Block Previous: 20d59499ef38bda24de15df140fd195b2627a9707453c6afd12458866ab5eba9
Block #3
Data {'action': 'buy', 'account': 'Winky', 'amount': 20}
Block Hash: 28bf741c567028c4a3f3975aacb6f7e23561d240f06608cd1241d308fe40557b
Block Previous: 0797ecc35e15f4758b635ee4053006bbb9a61ca9cba8876fbfa6d9a2c186a882
Block #4
Data {'action': 'buy', 'account': 'Xxz', 'amount': 4}
Block Hash: 29eae18d6f72bd2203c7a3fdce3f688178aae8b371fd530ddffa67a042be41c1
Block Previous: 28bf741c567028c4a3f3975aacb6f7e23561d240f06608cd1241d308fe40557b
Chain valid? True
Chain valid? False
</code></pre>

<h1>博客链接</h1>

<a href="https://xichunling.com/index.php/2018/10/29/%E7%94%A8python%E5%86%99%E4%B8%80%E4%B8%AA%E7%AE%80%E5%8D%95%E7%9A%84%E5%8C%BA%E5%9D%97%E9%93%BE/">传送门</a>


<h1>参考资料</h1>

<a href="https://blog.goodaudience.com/learning-about-block-chain-with-python-8b2178cf1fca" title="Learning about Block Chain with Python">Learning about Block Chain with Python</a>
