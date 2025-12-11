if [[ -z $1 ]]; then
	echo "Usage: $0 <input filename>"
	exit 1
fi

curl -X POST "http://localhost:8080/inference/" -H "accept: application/json" -H "Content-Type: multipart/form-data" -F "file=@$1"
