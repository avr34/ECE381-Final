if [[ -z "$1" || -z "$2" ]]; then
	echo "Usage: bash $1 <Path to file> <Output filename>"
	exit 1
fi

OUTPUT=$2

if [[ ! "$OUTPUT" == *.mp4 ]]; then
	OUTPUT="$OUTPUT.mp4"
	echo "Appended .mp4 to $2"
fi

curl -X POST "http://localhost:8000/inference/" -F "file=@$1" -o "$OUTPUT"
