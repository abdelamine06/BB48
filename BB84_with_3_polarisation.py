import sys
from math import ceil, log, sqrt
from random import randint, random, sample
from multiprocessing import Pool

Alice = {'randomBits':[], 'randomBases':[], 'selectedBits':[], 'selectedBases':[], 'finalKey':[]}
Bob = {'measuredBits':[], 'randomBases':[], 'selectedBits':[], 'selectedBases':[], 'finalKey':[]}
correct_basis_indices = []
BITSIZE = 0

def etape1():
    temp_bit_list = []
    temp_polarisation_list = []
    for i in range(0, BITSIZE):
        random_bit = randint(0,2)
        random_basis = randint(0,2)
        temp_bit_list.append(random_bit)
        if (random_basis == 0):
            temp_polarisation_list.append('X')
        elif (random_basis == 1):
            temp_polarisation_list.append('+')
        elif (random_basis == 2):
            temp_polarisation_list.append('Z')
            
    Alice['randomBits'] = temp_bit_list
    Alice['randomBases'] = temp_polarisation_list

def etape2_3():

    temp_bit_list_Bob = []
    temp_polarisation_list_Bob = []
    for i in range(0, BITSIZE):
        random_basis = randint(0,2)
        if (random_basis == 0):
            temp_basis = 'X'
        elif (random_basis == 1):
            temp_basis = '+'
        elif (random_basis == 2):
            temp_basis = 'Z'
        
        temp_polarisation_list_Bob.append(temp_basis)
        
        if (Alice['randomBases'][i] == temp_basis):
            temp_bit_list_Bob.append(Alice['randomBits'][i])
        else:
            temp_bit_list_Bob.append(randint(0,2))
            
    Bob['measuredBits'] = temp_bit_list_Bob
    Bob['randomBases'] = temp_polarisation_list_Bob
    
def etape4_5():
    for i in range(0, BITSIZE):
        if (Alice['randomBases'][i] == Bob['randomBases'][i]):
            correct_basis_indices.append(i)

def etape6_1(received):
    lower = received[0]
    upper = received[1]
    
    bit_list_alice = []
    basis_list_alice = []
    bit_list_bob = []
    basis_list_bob = []

    
    for i in range(lower, upper):
        if (i in correct_basis_indices):
            bit_list_alice.append(Alice['randomBits'][i])
            basis_list_alice.append(Alice['randomBases'][i])
            bit_list_bob.append(Bob['measuredBits'][i])
            basis_list_bob.append(Bob['randomBases'][i])
            
    return (bit_list_alice, basis_list_alice, bit_list_bob, basis_list_bob)      

def etape6_2():
    input = [(0, int(BITSIZE/6)), 
            (int(BITSIZE/6), int(2*BITSIZE/6)), 
            (int(2*BITSIZE/6), int(3*BITSIZE/6)), 
            (int(3*BITSIZE/6), int(4*BITSIZE/6)), 
            (int(4*BITSIZE/6), int(5*BITSIZE/6)), 
            (int(5*BITSIZE/6), BITSIZE)]
    
    pool = Pool(6)
    
    results = pool.map(etape6_1, input)
    
    temp_bit_list_alice =          results[0][0] + results[1][0] + results[2][0] + results[3][0] + results[4][0] + results[5][0]
    temp_polarisation_list_alice = results[0][1] + results[1][1] + results[2][1] + results[3][1]  + results[4][1] + results[5][1]
    temp_bit_list_bob =            results[0][2] + results[1][2] + results[2][2] + results[3][2] + results[4][2] + results[5][2]
    temp_polarisation_list_bob =   results[0][3] + results[1][3] + results[2][3] + results[3][3] + results[4][3] + results[5][3]
  
    Alice['selectedBits'] = temp_bit_list_alice
    Bob['selectedBits'] = temp_bit_list_bob
    Alice['selectedBases'] = temp_polarisation_list_alice
    Bob['selectedBases'] = temp_polarisation_list_bob
    
def PresentationBB84(bit_size):
    global BITSIZE
    BITSIZE = bit_size
    print("Bienvenue à la simulation du protocole BB84")
    input("Cliquez entrer pour proceder à la  1 étape...\n")
    
    print("Etape 1: Alice va préparer un random bits et les mesurés en deux bases soit X soit +")
    etape1()
    print("les bits et les bases d'alice:")
    print(Alice['randomBits'])
    print(Alice['randomBases'])
    input("Cliquez entrer pour proceder à la 2 étape...\n")
    
    print("Step 2: Alice envoi les qubits pour bob  (intercepter par eve)")
    print("Step 3: Bob mesure en random les qubits envoyés par alice soit par 'x' oubien '+' et renvoie ses resultat")
    etape2_3()
    
    print("Les bits et les bases de bob :")
    print(Bob['measuredBits'])
    print(Bob['randomBases'])
    input("Cliquez entrer pour proceder à la  4 étape ...\n")
    
    print("Step 4: Bob informe alice publiquement à partir de quelle base à mesurer chaque qubits")
    print("Step 5: Alice informe de sa part pour quel qubits à choisi à bien était mesuré par une meme base que la sienne" )
    etape4_5()
    print("Indices  bits/bases ou alice et bob ont choisi la meme base:")
    print(correct_basis_indices)
    input("Cliquez entrer pour proceder à la  6 étape...\n")
    
    print("Step 6: Alice et Bob enleve de leur liste tous les qubits identiques pour les quels les bases sont differente(causé par eve)")
    etape6_2()
    print("Bases et bits séléctionnés pour Alice:")
    print(Alice['selectedBits'])
    print(Alice['selectedBases'], "\n")
    print("Bases et bits séléctionnés pour Bob")
    print(Bob['selectedBits'])
    print(Bob['selectedBases'], "\n")
    print("Percentage de similarité: ", (len(Alice['selectedBits']))/BITSIZE*100,"%")
    
    
if __name__ == "__main__":
            print("Lancez le protocol BB84")
            userInput =  input("Combien de bits voullez vous tester? (Recommendez: petit)\n")
            PresentationBB84(int(userInput))   
        