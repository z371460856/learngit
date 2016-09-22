def historyDataInput():
	stopWord='endend'
	#when input 'endend' ,input end
	historyData=''
	for line in iter(input,stopWord):
		historyData+=line+'\n'
	historyDataList=historyData.split('\n')
	return historyDataList
	#examole historyDataList=['id1','time1','anId1 x1 y1','anId2 x2 y2','','id2','time2','anId3 x3 y3']

def dataPreProcess(hisData):
	m=0
	curAn={}
	#example curAn={'anId':[x,y]}
	result={}
	#example result={'id':curAn}
	for ele in hisData:
		if len(ele)==0:
			if m!=0:
				result[id]=curAn
				m=0
				continue
			else:
				continue
		else:
			if m==0:
				id=ele
				m=m+1
			elif m==1:
				time=ele
				m=m+1
			else:
				li=ele.split()
				anId=li[0]
				intxy=list(map(int,li[1:]))
				if len(intxy)==4:
					if anId not in curAn:
						return "Invalid format"
					else:
						if (intxy[0]!=curAn[anId][0]) or (intxy[1]!=curAn[anId][1]):
							#data false
							return "Conflict found at %s"%id
						else:
							dx=intxy[0]+intxy[2]
							dy=intxy[1]+intxy[3]
							curAn[anId]=[dx,dy]
				elif len(intxy)==2:
					curAn[anId]=[intxy[0],intxy[1]]
				else:
					return "Invalid format"
				m=m+1
	return result

def getSnapshot(processData,id):
	#processData=dataPreProcess(data)
	#preprocess historyData
	if id not in processData:
		return "id not in historyData"
	else:
		resultAn=processData[id]
		sortKey=sorted(resultAn.keys())
		for keyso in sortKey:
			print(keyso,resultAn[keyso][0],resultAn[keyso][1])


		#return resultAn
		'''
		resultAn=sorted(resultAn.iteritems(),key=lambda d:d[0])
		for animal in resultAn:
			print(animal)
			print('\n')
		'''









if __name__ == '__main__':
	history=historyDataInput()
	inputId=input("please input id:\n")
	proceData=dataPreProcess(history)
	if type(proceData) is dict:

		getSnapshot(proceData,inputId)
	else:
		print(proceData)


