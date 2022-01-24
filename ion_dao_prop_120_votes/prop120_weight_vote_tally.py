import subprocess, json, yaml
import pandas as pd

# with open("ion_dao_prop_120_votes/test.json","r") as file:
with open("ion_dao_prop_120_votes/prop120votes_block_2765219.json","r") as file:
    votes120 = json.load(file)
    votes120 = votes120["votes"]

def write_json(results_list):
    with open("ion_dao_prop_120_votes/prop120_vote_results.json", "w") as file:
        json.dump(results_list,file)

# Query node for a voters stake weight
def get_voter_weight(address,height):
    cmd = f"osmosisd q staking delegations {address} --height {height} -o json"
    output = subprocess.check_output(cmd, shell=True)
    output_dict = json.loads(output.decode("utf-8"))
    delegations = output_dict["delegation_responses"]
    stake_weight =0
    for delegation in delegations:
        stake_weight += int(delegation["balance"]["amount"])
    return stake_weight

# Reduce vote text
def vote_option(option):
    if option == "VOTE_OPTION_YES":
        return "YES"
    elif option == "VOTE_OPTION_NO":
        return "NO"
    elif option == "VOTE_OPTION_NO_WITH_VETO":
        return "VETO"
    elif option == "VOTE_OPTION_ABSTAIN":
        return "ABSTAIN"


# Last vote 120 block
height = 2765219
results_list = []
result = {}
i = 0
for vote in votes120:
    result["voter"] = vote["voter"]
    result["vote"] = vote_option(vote["option"])
    result["weight"] = get_voter_weight(vote["voter"],height)
    results_list.append(result.copy())

write_json(str(results_list))
df = pd.DataFrame(results_list)
df.to_csv('ion_dao_prop_120_votes/prop120_vote_results.csv')

# GET VOTES FOR THIS HEIGHT **INSTEAD OF PAGINATING I JUST DID A COUNT THEN QUERY WITH INCREASED LIMIT PARM
# osmosisd q gov votes 120 --height 2765219 --count-total
#   pagination:
#     next_key: FAQGdaCTlordzQNca86ZduEeT4Lw
#     total: "6249"     <====== total count of address"s that voted and how man results the limit parm needs to accept
# osmosisd q gov votes 120 -o json --height 2765219 --limit 10000 | jq  > prop120votes.json

