f = open('10evalrandom.txt')
f2 = f.readlines()
ided = 0
for x in f2:
	if '3' in x:
		ided +=1
print 'random',ided

f = open('10evalpred.txt')
f2 = f.readlines()
ided = 0
for x in f2:
	if '3' in x:
		ided +=1
print 'pred',ided

f = open('10evalmeme.txt')
f2 = f.readlines()
ided = 0
for x in f2:
	if '3' in x:
		ided +=1
print 'meme',ided