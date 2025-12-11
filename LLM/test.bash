if [[ -z $1 || -z $2 ]]; then
	echo "Usage: $0 <prompt> <max_tokens>"
	exit 1
fi

PROMPT="\"prompt\": \"User: $1. Assistant:\""
TOKENS="\"max_tokens\": $2"

curl -X POST "http://localhost:8000/inference/" -H "Content-Type: application/json" -d "{$PROMPT, $TOKENS}"
