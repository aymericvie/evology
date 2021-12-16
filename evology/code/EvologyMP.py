# import concurrent.futures
import multiprocessing as mp
from main import *
import time
# import warnings
# warnings.filterwarnings("ignore")
from main import main as evology
# df,pop = evology("static", 'scholl', 'newton', False, 75, 0, 3, 0, [1/3, 1/3, 1/3], True, False)

def job(iteration):
	df,pop = evology("static", 'scholl', 'newton', False, 1000, 0, 10, 0, [1/3, 1/3, 1/3], True, False)
	return df['WShare_NT'].iloc[-1]
	# return random.randint(0,10)

# print(do_something())

reps = 30

def main():
	start = time.perf_counter()
	p = mp.Pool()
	data = p.map(job, [i for i in range(reps)])
	p.close()
	print(data)
	print(len(data))
	finish = time.perf_counter()
	print(f'Multiprocessing () Finished in {round(finish-start, 2)} second(s)')

	start = time.perf_counter()
	data2 = []
	for i in range(reps):
		data2.append(job([]))
	finish = time.perf_counter()
	print(data2)
	print(len(data2))
	print(f'For loop Finished in {round(finish-start, 2)} second(s)')

if __name__ == '__main__':
	main()



# def main():
# 	reps = 10
# 	FinalResults = []
# 	# with concurrent.futures.ProcessPoolExecutor() as executor:
# 	with concurrent.futures.ProcessPoolExecutor() as executor:

# 		results = [executor.submit(do_something) for _ in range(reps)]

# 	for f in concurrent.futures.as_completed(results):
# 		# print(f.result())
# 		FinalResults.append(f.result())
# 	# print(type(results))
# 	del executor
# 	return FinalResults

# import multiprocessing as mp

# def main(): 
# 	reps = 10
# 	FinalResults = []
# 	processes = []
# 	for _ in range(10):
# 		p = mp.Process(target=do_something)
# 		p.start()
# 		processes.append(p)
# 	for process in processes:
# 		process.join()
# 		FinalResults.append(queue.get())
# 	return FinalResults
	
# '''
# start = time.perf_counter()
# if __name__ == '__main__':
# 	print(main())
# finish = time.perf_counter()
# print(f'Multiprocessing Finished in {round(finish-start, 2)} second(s)')

# def no_mp(reps):
# 	results = []
# 	for i in range(reps):
# 		# results.append(random.randint(0,10))
# 		results.append(do_something())
# 	return results

# start = time.perf_counter()
# no_mp(reps)
# finish = time.perf_counter()
# print(f'Enumeration Finished in {round(finish-start, 2)} second(s)')
# '''


