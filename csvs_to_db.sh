ls -d csv_dir/*|xargs -I{} python3 load_cyclone_history.py -file {}
