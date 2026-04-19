import subprocess
import os	

i=1
dim=range(1000, 7001, 1000)

for d in dim:

	blocks=range(5, 40, 5)
	for b in blocks:
		i+=1
		print(f"Running with dimension {d} and block size {b*d/100}, corrida {i}")

