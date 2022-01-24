import subprocess, json

# When vote results are not present in state for the queried block height the result is None/Null
def check_for_votes(height,prop_num):
    cmd = f'osmosisd query gov votes {prop_num} --height {height} -o json'
    output = subprocess.check_output(cmd, shell=True)
    output_dict = json.loads(output.decode('utf-8'))
    return output_dict

# Starting loop from close block height
height = 2765225
prop_num = 120

test = check_for_votes(height,prop_num)
# Init vote results
vote_results = None
# loop until we get a none back from checking the balance and confirm that no action has been taken 
while vote_results == None:
    vote_results = check_for_votes(height,prop_num)
    if vote_results is None:
        print(f'Prop #{prop_num} not present in state at height : {height}')
    else:
        print(f'Prop #{prop_num} results found in state at height : {height}')
    height -= 1

# Prop #120 not present in state at height : 2765220
# Prop #120 results found in state at height : 2765219