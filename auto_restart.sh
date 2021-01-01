until app.py; do
    echo "The main server is stopped unexpectedly with exit code: $?. Restarting..." >&2
    sleep 1
done