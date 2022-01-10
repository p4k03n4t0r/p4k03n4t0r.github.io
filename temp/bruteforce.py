from ansible_vault import Vault
from ansible.parsing.vault import AnsibleVaultError
import multiprocessing
import time


def try_password(encrypted, password, results_queue):
    vault = Vault(password)
    try:
        secrets = vault.load(encrypted)
        print(f"Password found: {password}")
        print(f"Decrypted file: {secrets}")
        results_queue.put(True)
    except AnsibleVaultError:
        pass


# from: https://github.com/OpenTaal/opentaal-wordlist
with open("wordlist.txt") as f:
    wordlist = f.read().split("\n")

with open("vault") as vault_file:
    vault_file_content = vault_file.read()

starttime = time.time()

# Set to max file descriptor limit: ulimit -n
# Increase it to the hard limit: sysctl -w fs.file-max=$(ulimit -Hn)
batch_size = 1000

for i in range(0, len(wordlist), batch_size):
    processes = []
    results_queue = multiprocessing.Queue()
    for j in range(0, batch_size):
        j = j + i
        if j >= len(wordlist):
            continue
        p = multiprocessing.Process(
            target=try_password, args=(vault_file_content, wordlist[j], results_queue)
        )
        processes.append(p)
        p.start()

    for process in processes:
        r = process.join()

    if not results_queue.empty():
        break

print("That took {} seconds".format(time.time() - starttime))
