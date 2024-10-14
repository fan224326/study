import tkinter as tk
from tkinter import messagebox
from web3 import Web3

# ERC-20代币的标准ABI，用于查询代币余额
erc20_abi = '''[
    {
        "constant": True,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "type": "function"
    }
]'''

# 初始化Web3连接
def init_web3(provider_url):
    web3 = Web3(Web3.HTTPProvider(provider_url))
    if web3.is_connected():
        return web3
    else:
        raise Exception("连接失败")

# 查询余额（ETH或代币）
def get_balances():
    try:
        # 获取用户自定义的URL
        provider_url = url_entry.get()
        web3 = init_web3(provider_url)

        # 获取代币合约地址
        token_address = token_entry.get().strip()

        # 获取用户输入的多个钱包地址，每行一个地址
        addresses = address_text.get("1.0", tk.END).strip().split('\n')
        result_text = ""

        for wallet_address in addresses:
            wallet_address = wallet_address.strip()

            if wallet_address:
                # 如果未输入代币合约地址，则查询ETH余额
                if not token_address:
                    balance = web3.eth.get_balance(wallet_address)
                    eth_balance = Web3.from_wei(balance, 'ether')
                    result_text += f"{wallet_address}: {eth_balance} ETH\n"
                else:
                    # 查询ERC-20代币余额
                    token_contract = web3.eth.contract(address=web3.toChecksumAddress(token_address), abi=erc20_abi)
                    balance = token_contract.functions.balanceOf(wallet_address).call()
                    token_balance = Web3.from_wei(balance, 'ether')
                    result_text += f"{wallet_address}: {token_balance} 代币\n"

        result_label.config(text=result_text)
    except Exception as e:
        messagebox.showerror("错误", f"无法获取余额: {e}")

# 创建窗口
root = tk.Tk()
root.title("自定义URL与ETH/代币的余额查询")

# 输入自定义URL
tk.Label(root, text="输入自定义节点URL:").grid(row=0)
url_entry = tk.Entry(root, width=50)
url_entry.grid(row=0, column=1)
url_entry.insert(0, "https://mainnet.base.org")  # 默认Base网络

# 输入代币合约地址（可选）
tk.Label(root, text="输入代币合约地址(留空查询ETH):").grid(row=1)
token_entry = tk.Entry(root, width=50)
token_entry.grid(row=1, column=1)

# 输入多个钱包地址，每行一个
tk.Label(root, text="输入钱包地址(每行一个地址):").grid(row=2)
address_text = tk.Text(root, height=10, width=50)
address_text.grid(row=2, column=1)

# 创建查询按钮
query_button = tk.Button(root, text="查询余额", command=get_balances)
query_button.grid(row=3, column=1)

# 显示结果的标签
result_label = tk.Label(root, text="")
result_label.grid(row=4, column=1)

# 运行窗口
root.mainloop()
