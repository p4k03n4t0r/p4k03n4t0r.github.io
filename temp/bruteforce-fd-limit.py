from ansible_vault import Vault
from ansible.parsing.vault import AnsibleVaultError
import multiprocessing
import time


def try_password(encrypted, password):
    vault = Vault(password)
    try:
        secrets = vault.load(encrypted)
        print(f"Password found: {word}")
        print(f"Decrypted file: {secrets}")
        return True
    except AnsibleVaultError:
        return False


# from: https://github.com/OpenTaal/opentaal-wordlist
# with open("wordlist.txt") as f:
with open("short_wordlist.txt") as f:
    wordlist = f.read().split("\n")

with open("vault") as vault_file:
    vault_file_content = vault_file.read()

    starttime = time.time()

    # for word in wordlist:
    #     found = try_password(vault_file_content, word)
    #     if found:
    #         break

    processes = []
    for word in wordlist:
        p = multiprocessing.Process(
            target=try_password, args=(vault_file_content, word)
        )
        processes.append(p)
        p.start()

    for process in processes:
        process.join()

    print("That took {} seconds".format(time.time() - starttime))
