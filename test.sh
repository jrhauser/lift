for file in ./test_systems/*/*/*/*; do
    ./lift $file timing123.csv
    echo $file
done