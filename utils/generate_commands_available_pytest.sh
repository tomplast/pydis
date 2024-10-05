for line in $(cat commands_availability.txt | grep ",1.0.0"); do
  command=$(echo $line | sed 's/,.*//')

  cat <<EOF
def test_command_${command}_is_available(client):
    assert(client.command_is_available("$command"))
EOF

  echo ""

done
