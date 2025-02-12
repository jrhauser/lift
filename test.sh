for file in ./test_systems/100/100/feasible/*; do
    ./lift $file timing.csv
done