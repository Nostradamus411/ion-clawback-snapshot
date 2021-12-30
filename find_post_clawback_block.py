import subprocess, json

# osmo1nju6ph47fcpu8ww5rra0d93c94v5mn87tefwu9 is an account which had it's OSMO clawed back

def get_osmos_bal(height):
    cmd = f'osmosisd q bank balances osmo1nju6ph47fcpu8ww5rra0d93c94v5mn87tefwu9 --height {height} --output json'
    output = subprocess.check_output(cmd, shell=True)
    output_dict = json.loads(output.decode('utf-8'))
    bal_list = output_dict["balances"]
    for coin in bal_list:
        if coin["denom"] == 'uosmo':
            bal = coin["amount"]
            return bal

# Sequence number of 0 means no tx have happened from the account ==> inferred unclaimed ion
def chain_action(height):
    cmd = f'osmosisd query auth account osmo1nju6ph47fcpu8ww5rra0d93c94v5mn87tefwu9 --height {height} -o json'
    output = subprocess.check_output(cmd, shell=True)
    output_dict = json.loads(output.decode('utf-8'))
    if int(output_dict['sequence']) > 0:
        return True
    else:
        return False

# Starting loop from close block height
height = 2397430
# Init bal to zero
bal = 0
# loop until we get a none back from checking the balance and confirm that no action has been taken 
while bal != None:
    bal = get_osmos_bal(height)
    made_action = chain_action(height)
    if bal is None and made_action is False:
        print('Post Clawback Block : ' + str(height))
    else:
        print('Not block - ' + str(height))
    height += 1