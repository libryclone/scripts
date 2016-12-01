#!/usr/bin/env python

import subprocess
import sys
import json


def run_command(cmd):
    """given shell command, returns communication tuple of stdout and stderr"""
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    return p.communicate()


# True = available, False = not available, None = no lbry sd hash value contained
def check_name(claim_name):
    arg_dict = json.dumps({"name": claim_name})
    out, err = run_command("lbrynet-cli get_claim_info '{}'".format(arg_dict))
    out = json.loads(out)

    if out is False:
        return None
    if not isinstance(out['value'], dict):
        try:
            out['value'] = json.loads(out['value'])
        except:
            return None

    try:
        if 'sources' not in out['value'] or 'lbry_sd_hash' not in out['value']['sources']:
            return None
    except TypeError:
        # print(out)
        return None

    sd_hash = out['value']['sources']['lbry_sd_hash']
    # print("SD HASH:{}".format(sd_hash))

    arg_dict = json.dumps({"sd_hash": sd_hash})
    out, err = run_command("lbrynet-cli download_descriptor '{}'".format(arg_dict))

    return bool(json.loads(out))


if len(sys.argv) >= 2:
    print check_name(sys.argv[1])
    sys.exit()

count = 0
available = 0
missing = 0
no_hash = 0


def print_status():
    print("STATUS: {} examined, {} available ({}%), {} missing ({}%), {} no_hash ({}%)".format(
        count, available, round(1.0 * available / count * 100, 1), missing,
        round(1.0 * missing / count * 100, 1), no_hash, round(1.0 * no_hash / count * 100, 1))
    )


with open('names.txt', 'r') as claim_list:
    for name in claim_list.readlines():
        name = name.strip()
        count += 1
        if name == '':
            continue
        sys.stdout.write("checking {} ... ".format(name))
        sys.stdout.flush()
        test = check_name(name)
        if test is None:
            print("no lbry_sd_hash")
            no_hash += 1
        elif test is True:
            print("available")
            available += 1
        elif test is False:
            print("missing")
            missing += 1
        else:
            raise TypeError("unknown return type: %r".format(test))

        if count % 20 == 0:
            print_status()

print_status()
