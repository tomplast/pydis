rm commands_availability.txt || touch commands_availability.txt
for command in $(curl -s https://redis.io/docs/latest/commands/ | sed -n 's/^.*href="\(\/docs\/latest\/commands\/.*\)".*$/\1/p'); do

  if [ "${#command}" -lt 25 ]; then
    continue
  fi

  available_since=$(curl -s https://redis.io$command | grep "Available since:" -A 1 | sed -n 's/^.*>\([a-zA-Z0-9\.]*\)<\/dd>/\1/p')
  command_name=$(echo $command | sed 's/.*commands//' | tr '/' '\0')
  echo $command_name,$available_since >>commands_availability.txt
done
