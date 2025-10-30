from datetime import time
import os
import json
from web3 import Web3

# Подключение к локальному Ganache
ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

# Проверим соединение
if not web3.is_connected():
    raise ConnectionError("Не удалось подключиться к Ganache")

# Путь к build/contracts/PostContract.json
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTRACT_JSON_PATH = os.path.join(BASE_DIR, 'eth_contracts', 'build', 'contracts', 'PostContract.json')

# Загрузка ABI и адреса
with open(CONTRACT_JSON_PATH) as f:
    contract_json = json.load(f)
    abi = contract_json['abi']

    # Получаем адрес контракта из сети 5777 (это Ganache по умолчанию)
    networks = contract_json.get('networks')
    if not networks or '5777' not in networks:
        raise ValueError("Смарт-контракт не был задеплоен в сеть 5777. Проверь truffle migrate.")
    
    contract_address = networks['5777']['address']
    contract_address = web3.to_checksum_address(contract_address)

# Инициализация контракта
contract = web3.eth.contract(address=contract_address, abi=abi)

# Пример функции: создать пост
def create_post_on_chain(content, sender_address, private_key):
    nonce = web3.eth.get_transaction_count(sender_address)

    txn = contract.functions.createPost(content).build_transaction({
        'from': sender_address,
        'nonce': nonce,
        'gas': 3000000,
        'gasPrice': web3.to_wei('20', 'gwei'),
    })

    signed_txn = web3.eth.account.sign_transaction(txn, private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)

    tx_receipt = None
    while tx_receipt is None:
        try:
            tx_receipt = web3.eth.get_transaction_receipt(tx_hash)
        except:
            time.sleep(1)

    # Теперь ловим событие PostCreated из receipt
    logs = contract.events.PostCreated().process_receipt(tx_receipt)
    if logs:
        event = logs[0]['args']
        post_id = event['id']
        return {
            'tx_hash': web3.to_hex(tx_hash),
            'post_id': post_id
        }

    return None

# 🔹 Получение одного поста
def get_post_from_chain(post_id):
    try:
        post_data = contract.functions.getPost(post_id).call()
        return {
            'id': post_data[0],
            'author': post_data[1],
            'content': post_data[2],
        }
    except Exception as e:
        return {"error": str(e)}


# 🔹 Получение всех постов
def get_all_posts():
    try:
        count = contract.functions.getAllPosts().call()
        all_posts = []
        for i in count:
            all_posts.append({
                'blockchain_id': i[0],
                'author': i[1],
            })
        return all_posts
    except Exception as e:
        return {"error": str(e)}
