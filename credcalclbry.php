#!/usr/bin/php
<?php


# http://stackoverflow.com/a/1624602/6614049 and https://www.akalin.com/computing-isqrt
# converges on the floor() of the square root of $number
#function safeSqrt($number) {
#  $bits = strlen(decbin($number));
#  $x = 2**ceil($bits/2);
#  while (true) {
#    $y = floor(($x + floor($number/$x))/2);
#    if ($y >= $x) {
#      return $x;
#    }
#    $x = $y;
#  }
#}

function getReward($block) {
  if ($block == 0) {
    return 400000000;
  }
  elseif ($block <= 5100) {
    return 1;
  }
  elseif ($block <= 55000) {
    return 1 + floor(($block - 5001) / 100);
  }
  else {
    return max(0, 500 - floor(((sqrt(($block - 55001) / 4 + 1)) - 1) / 2));
  }
}


function getTotalReward($fromBlock, $toBlock) {
  if ($toBlock < $fromBlock) return 0;
  return array_sum(array_map('getReward', range($fromBlock,$toBlock)));
}



$blockTime = 160.9;
$start = 1466646588;
$now = gmdate('U');

$blocksNow = floor(($now - $start) / $blockTime);

$arg = isset($_SERVER['argv'][1]) ? $_SERVER['argv'][1] : 'now';

if (preg_match('/^\d+b$/', $arg)) {
  $blocksAtTarget = (int)substr($arg,0,-1);
  $target = $start + $blocksAtTarget*$blockTime;
}
else {
  $target = gmdate('U', strtotime($arg));
  $blocksAtTarget = floor(($target - $start) / $blockTime);
}

echo "Start: $start (" . date('Y-m-d H:i:s', $start) . ")\n";
echo "Now: $now (" . date('Y-m-d H:i:s', $now) . ")\n";
echo "Target: $target (" . date('Y-m-d H:i:s', $target) . ")\n";

echo "\n";

echo "Blocks now (assuming {$blockTime} seconds per block): " . number_format($blocksNow) . "\n";
echo "Credits now (assuming {$blockTime} seconds per block): " . number_format(getTotalReward(1,$blocksNow)) . "\n";

echo "\n";

echo "Blocks at target: " . number_format($blocksAtTarget) . "\n";
echo "Credits from now to target: " . ($blocksNow>$blocksAtTarget ? 0 : number_format(getTotalReward($blocksNow,$blocksAtTarget))) . "\n";
echo "Credits at target: " . number_format(getTotalReward(1,$blocksAtTarget)) . "\n";
echo "Reward of target block: " . number_format(getReward($blocksAtTarget)) . "\n";
