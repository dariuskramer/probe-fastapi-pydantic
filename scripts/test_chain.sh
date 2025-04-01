#!/usr/bin/env sh

set -o errexit
set -o nounset

host='127.0.0.1:8000'

curl --silent "${host}/entropy/generate/256" |
	curl --silent -H 'Content-Type: application/json' --data '@-' "${host}/seed/from_entropy/" |
	jq --raw-output '.seed' | tr -d '\n' |
	curl --silent --variable 'seed@-' --expand-url "${host}/keypair/from_derivation/m/1'/2/3'/4?seed={{seed}}"
