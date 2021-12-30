import pandas as pd
import json

# with open("test.json","r") as file:
with open("derived_balances_2397435.json","r") as file:
    snapshot = json.load(file)    
 
with open("osmosis-1.assetlist.json","r") as file:
    assetlist_json = json.load(file)
    assetlist = assetlist_json['assets']

# Getting dict's for exponents and denom names
list_len = len(assetlist)
ibc_list = []
ibc_denom_list = []
ibc_denom_dict = {}
ibc_exp_dict = {}

i = 0
while i < list_len:
    asset = assetlist[i]
    denom_l = asset['denom_units'][0]['denom']
    denom_h = asset['denom_units'][1]['denom']
    exponent = asset['denom_units'][1]['exponent']
    ibc_list.append({denom_l : denom_h})
    ibc_denom_list.append(denom_l)
    ibc_denom_dict[denom_l] = denom_h
    ibc_exp_dict[denom_l] = exponent
    i += 1
# Convert to a set to be able to check if denoms are IN the list of known assets
ibc_denom_set = set(ibc_denom_list)

accounts = snapshot["accounts"]

# Remove Module accounts containing ION (pools + lockup module) - except for the community pool
mod_accts = ['osmo1njty28rqtpw6n59sjj4esw76enp4mg6g7cwrhc',
'osmo1500hy75krs9e8t50aav6fahk8sxhajn9ctp40qwvvn8tcprkk6wszun4a5',
'osmo1zka4v4c04jr74ludyls2lfzfttzx67qzd070xtnfq90yzyacgn9qv6vend',
'osmo1kpf2xfutvfqfum9aj2juvjcjcxzp7k3le389v6ql6lurzcq0hausa6uyx8',
'osmo17ff0mxg5j6xtuh7ma623ejcntuzuvpewu9dyjk00wkadh75au3qs0gp8pv',
'osmo1d0elgsavwgez5xf0fdan3krzfjm5jkdtcgxzlvunu4jndycs8u8qzs5h33',
'osmo1a6rvlkd2jw32mjf2pt78fte7f2hqu7gvr0yqsqek2c7anftrunkqqq798z',
'osmo1hpfr8caa9swnqj2wapqwjfakqkfvdq70uvjv37pdst3xunsde2hqkz0na4',
'osmo18yxeq5kpup4k47vhjgu8j4y8d82sna7sdtjlz7hkuphnqtsmh8asc9vgca',
'osmo1pppq6lxkyrhh74npg87t2hgzqvamdck0u2qkycptdlczpx95h9tqn4c8d3',
'osmo1p9pa7umdvry4u4338hgu4x5pkepnk9pcqddpg65zdj0k3a3ucjts85hj73',
'osmo1r57khl30h7ewsqe0lkr4kk7m58nlsg2qjzgxzsjal2jec9q3xcnqshf4sn',
'osmo1l5ehe7cqgf5fplxegqaukwygaz8g2h62yhdt06te6uem30l2j9mswf6qct',
'osmo106vz3g36x84avkrrt2v602khu0t9lppptdd2gp0mr0l35pmqv5fqe2wmhj',
'osmo14rjjpwlhg3vdqtuvjx7jkfnvas3uhhyak4r6pnewup00qm0thjmsstmrv2',
'osmo1r32kkdc46p78k6lsaqld3dl7dvdquunue3w60amuylg8q945mqzqehqgcs',
'osmo1ztk3sfcrdvv2lnmjzfad5qerkevp3y5ny8s3n5t8c94pxwu0putqw3dqtw',
'osmo1hjkkjcc88t8mf2h4n2rzdxtdpmscv53ek33vs48jxk5x0d2uf9hs59teze',
'osmo15eqya8as2ytwxzwfeyjs0xra4yxdeakp70397fzvhfa0vf0z3lmslnkzgv',
'osmo1efs9dkdr9qtk85e69ah5nzng60wtz04yhh05vnq7l3vcvy38aj2snmr8r7',
'osmo18pr2rasc9428jwr6t8hf4m50fgd35am4s6lr45yae0slmfzqukgq20jmsw',
'osmo1k33jzr6syz8fs9jlsjerwum53ctu9nzkfdr3uy58ddt2tpsnsw0sl8ff3s',
'osmo1dyvjg5eyr58e73fpnw3z6c7wz2h0wvarmpmvq0c60vawm8e6q70q44v94n',
'osmo1f33v0n0kn6vtu7vkxuf2rm9dxncnwuga5825tzupc3t9umsgt0rsl6u29e',
'osmo1m4qg2yg542hp38yrdnp7wxhpm8j3agu78sg7f6lz0dzpmk4t4cysy9x5mj',
'osmo1daztxlwd90kqt7yw7mvakhp9kjd34g250dywutq06nvlze2u6uhsuk26xw',
'osmo132qw6zaztxfnjj3a2e20adm3xwzjrycqwcc048x6wpv0w00dgl7qvlln2p',
'osmo13cslqv80p4uzx4cxjvpnrva68yac6z55yhafqau3k5vy6yw5027q2yx8ms',
'osmo1gjfqv5vtwnm99dwac9v9ug4l9msyq9wejnatnvj35ex25ak2nrssh3pat9',
'osmo19ffd2uz59gf0w594hpwxjgzrkt3c2vd70gzw6lhdtsz07hl2m7sqfky68k',
'osmo10v35xj20k0jrfgs8p3lqt5gyga0wug3kkh4pq6xt3x4hqh5huvcssp04d3',
'osmo1u6wc5hkhg50kxdn9l8pye6zt6jvh5czeej86r4c6segzt0sw6wnsn7rj2x',
'osmo12huxa5wnwskf8mnmr096yzwyrehm970782j95h25uuxrxxz8wdpq7udusr',
'osmo13u649up5fe79u2aq0d3rsl5x48lulu5yred75lcuw94dlugfxdqq39hz0s',
'osmo1pul0yh6cr9wa6xghehfc8z8cx94krfm065v59r2py5clyqnfq7hq7yt77f',
'osmo13nztwp3wht4k8zm6ztkczjqxyu74kvl8xjjfqssd7g2lwghzknhqn9gpek',
'osmo17rujtwmvk8vp3uqq6xxkymk83n3qethhejuar7ayhyuupcsw66mqmg4k28',
'osmo1szh2gzzsugx6e5vs7emkcrmcy87zg75jst8xemdp896v33u5f5eqt395ku',
'osmo1a0ev3jr6fts7y09as95pryn59hzwfkaletpusfzctejjy0wqa47sxqgy3a',
'osmo1m06zu73wfy99eaxhlzy7mcgwz6lfhs3whse0978wjk66s057h9yswfmgzf',
'osmo1d7p44gdu45sp4jh4r5a8jppvvlrf3jd4synudv3kwa8lhz2clhzsnq04ed',
'osmo1ejcrrmfxaphd6nf270r34467u2a407mewhq5g5cz6hdhzqs7nnxsvpthf9',
'osmo14sxd3nugue3z44lh55cvn7uq8xzzzkgfknnuxtazr569jyymcqys2eykgs',
'osmo16qzex7q0cpj3dflx79ycqvsujm0dt838lfjv9fjg80zna7jpn2ssn3cta4',
'osmo1c2pg9y4evezv5twrpfecc78yslp467ea896zls960ptsre88c07qdpanaj',
'osmo1r5v05r30s0v75py3n3lhd7sq5cdgkaltles5rk0cmgndrdq7ktxqcn64y8',
'osmo1tz8jzsa8hlp3qc25l6wduxz3kyqvqa0l9sxwtqt5l9ur6rtqsrfsjk9rta',
'osmo18vt7x9yuda579ssr668avfe8mlngrf255fx3re23340twmh3ujyqsfr3h8',
'osmo157yhlzsnqxvrne3wdpukh7uca40l9mak875u44f9asufvwkldzzs7tpaal',
'osmo1k4gj3utpx0s3pmtq7shmyhdq2dp605e03hcprvzvec7jq2ge2u7s4r0wp4',
'osmo16dn4uk4xlqshzufy3f0as2pnvdpwqlwepp0m5qumwh2c4vgmp9jqaa0zsh',
'osmo1s46juu2q7ets8tgqaytaaekfs5qu259tkex87ll068xsvfcf8uas6rkavc']

mod_i = 0
for address in mod_accts:
    try:
        del accounts[mod_accts[mod_i]]
    except:
        pass
    mod_i += 1

list_by_addr = []
for account in accounts:

    # Single OsmoAddress to produce a 'row'
    acct_dict = accounts[account]
    # New dict structure to normalize the nested balances/bonds to columns
    new_acct_dict = {}

    # Define key column / index - OsmoAddress
    new_acct_dict['address'] = acct_dict['address']
    new_acct_dict['staked'] = int(acct_dict['staked']) / 10**6
    new_acct_dict['unstaked'] = int(acct_dict['unstaked']) / 10**6
    
    # unclaimed denom convert up
    for unclaim in acct_dict['unclaimed_airdrop']:
        base_denom = unclaim['denom']
        numerator = int(unclaim['amount'])
        denominator = 10**ibc_exp_dict[base_denom]
        full_denom = ibc_denom_dict[base_denom]
        full_denom_bal = numerator / denominator
        new_acct_dict['unclaimed_airdrop'] = full_denom_bal 

    # Loop through all balances of base denoms and calculate full denom amount adding as keys to new account dict
    for bal in acct_dict['balance']:
        # Excluding weird tokens not defined in osmosis-1.assetlist.json
        if bal['denom'] in ibc_denom_set:
            base_denom = bal['denom']
            numerator = int(bal['amount'])
            denominator = 10**ibc_exp_dict[base_denom]
            full_denom = ibc_denom_dict[base_denom]
            full_denom_bal = numerator / denominator
            new_acct_dict[full_denom+'-bal'] = full_denom_bal   

    for bond in acct_dict['bonded']:
        # Excluding weird tokens not defined in osmosis-1.assetlist.json
        if bond['denom'] in ibc_denom_set:
            base_denom = bond['denom']
            numerator = int(bond['amount'])
            denominator = 10**ibc_exp_dict[base_denom]
            full_denom = ibc_denom_dict[base_denom]
            full_denom_bond = numerator / denominator
            new_acct_dict[full_denom+'-bond'] = full_denom_bond    

    for tot in acct_dict['total_balances']:
        # Excluding weird tokens not defined in osmosis-1.assetlist.json
        if tot['denom'] in ibc_denom_set:
            base_denom = tot['denom']
            numerator = int(tot['amount'])
            denominator = 10**ibc_exp_dict[base_denom]
            full_denom = ibc_denom_dict[base_denom]
            full_denom_bond = numerator / denominator
            new_acct_dict[full_denom+'-total'] = full_denom_bond    
    list_by_addr.append(new_acct_dict)


df = pd.DataFrame(list_by_addr)
df = df.fillna(0)
# Find rows without any ion holdings
no_ion = df[ df['ion-total'] == 0 ].index
# Drop non-ion holding addresses
df.drop(no_ion, inplace=True)

# flat_snapshot = df.to_csv('test.csv', float_format='%.9f', index = False)
flat_snapshot = df.to_csv('ion_clawback_snapshot.csv', float_format='%.9f', index = False)
