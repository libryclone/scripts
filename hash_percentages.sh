#!/bin/bash

#email: grin@lbry.io, pass: vLaZ0uPoGaa&#d8PCXhU&AwP9%N1ueRXnfw, pin: 1359, username: lbry
coinmine=$(curl -s 'https://www2.coinmine.pl/lbc/index.php?page=api&action=getpoolstatus&api_key=b443b6c571aeb595b8599bc84a435f27de972aeb702a1aacd4662825b7f498f3&id=12856' | jq .getpoolstatus.data.hashrate)
#email: grin@lbry.io, pass: 7#lmGwzOLdp0klDolFvN178Is5VIwoo%UWB, pin: 1359, username: lbry
suprnova=$(curl -s 'https://lbry.suprnova.cc/index.php?page=api&action=getpoolstatus&api_key=1029640d6f3334436dcdff26f322d6405cda31c940873d51753f30daa186f446&id=317550' | jq .getpoolstatus.data.hashrate)
#email: grin@lbry.io, pass: ipiYjZbaj8T1HJbv^jhBDxUxR^oI34QiIm4, pin: 1359, username: lbryio
poolmn=$(curl -s 'https://pool.mn/lbry/index.php?page=api&action=getpoolstatus&api_key=d235b4248663929c549d0e5e8cc93684a5620f358eb2955488a3e734178a7ad5&id=8196' | jq .getpoolstatus.data.hashrate)

echo "coinmine: $coinmine"
echo "suprnova: $suprnova"
echo "poolmn: $poolmn"
