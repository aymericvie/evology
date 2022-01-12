import multiprocessing as mp
import sys
sys.path.append('evology/code')
from main import *
import time
import pandas
from main import main as evology

reps = 100
iterations = 25000
agents = 100

def job(iteration):
	df,pop = evology("static", 'scholl', 'esl.true', False, iterations, 0, agents, 0, [1/3, 1/3, 1/3], True, False)
	return df['WShare_NT'], df['WShare_VI'], df['WShare_TF']

def main():
	start = time.perf_counter()
	p = mp.Pool()
	data = p.map(job, [i for i in range(reps)])
	p.close()
	print(data)
	print(len(data))
	data = np.array(list(data))
	finish = time.perf_counter()
	print(f'Multiprocessing () Finished in {round(finish-start, 2)} second(s)')
	return data

if __name__ == '__main__':
	dataRun = main()
	# dataRun.tofile('evology/data/MonteCarloData.csv', sep = ',')
	print(type(dataRun))
	print(dataRun.shape)
	print(type(dataRun[0,0]))
	print(dataRun[0,0].shape)

	dfNT = pd.DataFrame()
	dfVI= pd.DataFrame()
	dfTF = pd.DataFrame()

	for i in range(reps):
		name = 'Rep%s' % i
		dfNT[name] = dataRun[i,0]
		dfVI[name] = dataRun[i,1]
		dfTF[name] = dataRun[i,2]

	dfNT.to_csv("evology/data/MC_NT.csv")
	dfVI.to_csv("evology/data/MC_VI.csv")
	dfTF.to_csv("evology/data/MC_TF.csv")

	plt.plot(dataRun[0,0], label = 'NT')
	plt.plot(dataRun[0,1], label = 'VI')
	plt.plot(dataRun[0,2], label = 'TF')
	plt.legend()
	plt.show()


''' 
Script to compare speed, mp vs non mp
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
	'''