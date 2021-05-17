#!/bin/sh

rm -rf /tmp/pokemon
mkdir -p /tmp/pokemon/

for i in `seq 1 898`
do
  if [ $i -lt 10 ]; then
    num="00$i"
  elif [ $i -lt 100 ]; then
    num="0$i"
  else
    num="$i"
  fi

  #echo $num

  target=`curl https://zukan.pokemon.co.jp/detail/$num -s | grep "og.*images/index" | awk '{ print $3 }' | awk -F '"' '{ print $2 }'`
  wget $target -O /tmp/pokemon/$num.jpg

done
