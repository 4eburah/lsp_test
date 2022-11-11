for y in 2013 2014 2015
do
	for m in 01 02 03 04 05 06 07 08 09 10 11 12
	do
		echo $y$m
		python3 cyclones_to_csv.py -month $y$m
	done
done

