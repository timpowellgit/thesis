from tabulate import tabulate
import re




f = open('scorefile70.txt')
lines = f.readlines()


table = []
for line in lines[:100]:
	strength,word = line.split(',')[0],line.split(',')[1]
	
	predictor = re.sub(r"(']|^\su')", "", word)
	score = re.sub(r"^\[", '', strength)
	pred =r'%s' %(predictor[:-1].decode('unicode-escape'))
	sp= score[:4] + ' ' + pred
	table.append(sp)

newtable = [[x, table[25:50][i], table[50:75][i], table[75:][i] ]for i,x in enumerate(table[0:25])]
print tabulate(newtable, tablefmt="latex")