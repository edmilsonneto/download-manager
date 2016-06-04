install:
	pip install -r requiriments.txt
run:
	mpirun -np 5 python  main.py