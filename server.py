import numpy as np
from random import randint
import socket
import time
import select


host = '127.0.0.1'

port = 7777

participants = []

scores = []

dat = []


QUE = ["The founder of www ? \nA.NewTon  \nB. steve jobs  \nC.Tim berners lee  \nD. Tesla\n",
		 "who is father of geometry? \nA.Siphon Action  \nB.Viscocity of Ink  \nC.Euclid \nD.Diffusion of ink through blotting \n",
		 "Light year is a unit of ? \nA.Time  \nB.Distance  \nC.light  \nD.Intensity of light\n",
		 "Mirage is due to ?  \nA.depletion of ozone layer in the atmosphere  \nB.magnetic disturbances in the atmosphere \nC. equal heating of different parts of the atmosphere   \nD.unequal heating of different parts of the atmosphere\n",
		 "Integral sinx?  \nA.cosx  \nB.tanx  \nC.cosx  \nD.-cosx\n",
		 "Pa(Pascal) is the unit for?  \nA.Thrust  \nB.Pressure  \nC.Conductivity  \nD.Frequency\n",
		 "time for maggi to cook!!!  \nA.4 minutes  \nB.2 minutes  \nC.8 minutes  \nD.16 minutes\n",
		 "Metals are good conductors of electricity because? \nA.the atoms are lightly packed  \nB.they contain free electrons   \nC.they have high melting point  \nD.All of the above\n",
		 "what is the area of a circle?  \nA.2*pi*r  \nB.pi*r*r  \nC.r*r  \nD.r*r*r\n",
		 "Who is the Father of computers?  \nA.Charles babbage  \nB.C V Raman  \nC.Steve jobs  \nD.Bill Gates\n The founder of www ? \nA.NewTon  \nB. steve jobs  \nC.Tim berners lee  \nD. Tesla\n",
                 "who is father of geometry? \nA.Siphon Action  \nB.Viscocity of Ink  \nC.Euclid \nD.Diffusion of ink through blotting \n",
                 "Light year is a unit of ? \nA.Time  \nB.Distance  \nC.light  \nD.Intensity of light\n",
                 "Mirage is due to ?  \nA.depletion of ozone layer in the atmosphere  \nB.magnetic disturbances in the atmosphere \nC. equal heating of different parts of the atmosphere   \nD.unequal heating of different parts of the atmosphere\n",
                 "Integral sinx?  \nA.cosx  \nB.tanx  \nC.cosx  \nD.-cosx\n",
                 "Pa(Pascal) is the unit for?  \nA.Thrust  \nB.Pressure  \nC.Conductivity  \nD.Frequency\n",
                 "time for maggi to cook!!!  \nA.4 minutes  \nB.2 minutes  \nC.8 minutes  \nD.16 minutes\n",
                 "Metals are good conductors of electricity because? \nA.the atoms are lightly packed  \nB.they contain free electrons   \nC.they have high melting point  \nD.All of the above\n",
                 "what is the area of a circle?  \nA.2*pi*r  \nB.pi*r*r  \nC.r*r  \nD.r*r*r\n",
                 "Who is the Father of computers?  \nA.Charles babbage  \nB.C V Raman  \nC.Steve jobs  \nD.Bill Gates\n"]

answer_list = ['C','C','B','D','B','B','B','B','B','A','C','C','B','D','B','B','B','B','B','A'] 

question_done = [0,0,0,0,0,0,0,0,0,0]

def rand_q(questions,answers):
	k = randint(0,len(questions)-1)
	if(question_done[k] != 0):
		while(question_done[k] != 0):
			k = randint(0,len(questions)-1)
		question_done[k] = 1
	else:
		question_done[k] = 1
	print(questions[k])
	return(k)

def answer_check(answers,buff,i):
	for ans in buff:
		if(answers[i] in ans[0]):
			index = participants.index((ans[1],ans[2]))
			scores[index] += 1
			break;

def final_scores(scores):
	print("The scoress are {}".format(scores))

	maxi = max(scores)
	if(scores.count(maxi)==1):
		print("The winner is {}".format(dat[scores.index(max(scores))]))
	else :
		winners = []
		for i in range(len(scores)):
			if(scores[i]==maxi):
				winners.append(dat[i])
		print("The winners are {}".format(winners))


s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

s.bind((host,port))

print "Server Started !!!"

start_time = 20

maxparticipants = 5

while(start_time>0 and len(participants)<maxparticipants):
	try:
		ready = select.select([s],[],[],1)
    	        '''print(ready[0])'''
		if(ready[0]):
			data , addr = s.recvfrom(1024)
			dat.append(data)
			print "Connected to {} ".format(data)
			if(addr not in participants):
				participants.append(addr)
				scores.append(0)
				print "{} participants in lobby".format(len(participants))
				for i in range(len(participants)):
					try:
						s.sendto("{} participants in lobby".format(len(participants)), participants[i])
					except:
						pass
				print(participants)

		start_time = start_time - 1
	except:
		pass


print("Game Starting . . .")

for i in range(len(participants)):
    try:
        s.sendto("Game starting . . .", participants[i])
    except:
        pass


buff = []

flag = 0

for i in range(10):
	if(flag==1):
		break

	try:
		buff = []
		print("Question no {}".format(i+1))
		curr_q = rand_q(QUE,answer_list)
		agiven = ""
		for i in range(len(participants)):
        		s.sendto(str(QUE[curr_q]),participants[i])
		ready = select.select([s],[],[],20)
		if(ready[0]):
			agiven,addr = s.recvfrom(1024)
			buff.append((agiven[len(agiven)-1:],addr[0],addr[1]))
			for i in range(len(participants)):
    				try:
        				if(participants[i] != addr):
						s.sendto("Too slow",participants[i])
    				except:
        				pass
		print("Answer given: {}".format(agiven))
		#print(buff)
		answer_check(answer_list,buff,curr_q)
		print(scores)
		for i in range(len(scores)):
			if(scores[i]==5):
				flag = 1
	except:
		pass

for i in range(len(participants)):
    try:
	if(scores[i] == max(scores)):
		s.sendto("Game Over\nYour scores {}\n\nYou win!!!".format(scores[i]), participants[i])
	else:
		s.sendto("Game Over\nYour scores {}\n\nYou lose!!!".format(scores[i]), participants[i])
    except:
        pass

final_scores(scores)
s.close()
