#!/bin/bash
echo "Contraseña para tor"
cat /etc/tor/torrc >> /etc/tor/torrc.back
read password
hash=$(tor --hash-password "$password")
hash=$(echo $hash|awk 'NF>1{print $NF}')
while read line
do
  if [[ $line == "#ControlPort 9051" ]]; then
    line="ControlPort 9051"
  elif [[ $line == *"#HashedControlPassword"* ]]; then
    line="HashedControlPassword "$hash
  fi
  echo $line >> new
done < /etc/tor/torrc
cat new > /etc/tor/torrc
rm new
echo "Reinice el servicio tor para que los cambios surtan efecto"
