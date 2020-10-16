
from math import ceil, log, sqrt
from random import randint, random, sample
from multiprocessing import Pool

Alice = {'randomBits':[], 'randomBases':[], 'selectedBits':[], 'selectedBases':[], 'finalKey':[]}
Bob = {'measuredBits':[], 'randomBases':[], 'selectedBits':[], 'selectedBases':[], 'finalKey':[]}
Eve = {'measuredBits':[], 'randomBases':[], 'selectedBits':[], 'selectedBases':[]}
Eva = {'measuredBits':[], 'randomBases':[], 'selectedBits':[], 'selectedBases':[]}

correct_basis_indices = []
BITSIZE = 0

def etape1():
    temp_bit_list = []
    temp_polarisation_list = []
    for i in range(0, BITSIZE):
        random_bit = randint(0,1)
        random_basis = randint(0,1)
        temp_bit_list.append(random_bit)
        if (random_basis == 0):
            temp_polarisation_list.append('X')
        elif (random_basis == 1):
            temp_polarisation_list.append('+')
            
    Alice['randomBits'] = temp_bit_list
    Alice['randomBases'] = temp_polarisation_list

def etape2_3():
    #aller de alice vers eve
    temp_bit_list_Eve = []
    temp_polarisation_list_Eve = []
    for i in range(0, BITSIZE):
        random_basis = randint(0,1)
        if (random_basis == 0):
            temp_basis = 'X'
        elif (random_basis == 1):
            temp_basis = '+'
        
        temp_polarisation_list_Eve.append(temp_basis)
        
        if (Alice['randomBases'][i] == temp_basis):
            temp_bit_list_Eve.append(Alice['randomBits'][i])
        else:
            temp_bit_list_Eve.append(randint(0,1))
            
    Eve['measuredBits'] = temp_bit_list_Eve
    Eve['randomBases'] = temp_polarisation_list_Eve
    
    # faire la meme chose mais de eve vers eva 
    temp_bit_list_Eva = []
    temp_polarisation_list_Eva = []
    for i in range(0, BITSIZE):
        random_basis = randint(0,1)
        if (random_basis == 0):
            temp_basis = 'X'
        elif (random_basis == 1):
            temp_basis = '+'
        
        temp_polarisation_list_Eva.append(temp_basis)
        
        if (Eve['randomBases'][i] == temp_basis):
            temp_bit_list_Eva.append(Eve['measuredBits'][i])
        else:
            temp_bit_list_Eva.append(randint(0,1))
            
    Eva['measuredBits'] = temp_bit_list_Eva
    Eva['randomBases'] = temp_polarisation_list_Eva
    # faire la meme chose mais de eve vers bob
    temp_bit_list_Bob = []
    temp_polarisation_list_Bob = []
    for i in range(0, BITSIZE):
        random_basis = randint(0,1)
        if (random_basis == 0):
            temp_basis = 'X'
        elif (random_basis == 1):
            temp_basis = '+'
        
        temp_polarisation_list_Bob.append(temp_basis)
        
        if (Eve['randomBases'][i] == temp_basis):
            temp_bit_list_Bob.append(Eva['measuredBits'][i])
        else:
            temp_bit_list_Bob.append(randint(0,1))
            
    Bob['measuredBits'] = temp_bit_list_Bob
    Bob['randomBases'] = temp_polarisation_list_Bob
    
    temp_bit_list_Bob = []
    temp_polarisation_list_Bob = []
    for i in range(0, BITSIZE):
        random_basis = randint(0,1)
        if (random_basis == 0):
            temp_basis = 'X'
        elif (random_basis == 1):
            temp_basis = '+'
        
        temp_polarisation_list_Bob.append(temp_basis)
        
        if (Eve['randomBases'][i] == temp_basis):
            temp_bit_list_Bob.append(Eve['measuredBits'][i])
        else:
            temp_bit_list_Bob.append(randint(0,1))
            
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
    bit_list_eve = []
    basis_list_eve = []
    bit_list_eva = []
    basis_list_eva = []
    
    for i in range(lower, upper):
        if (i in correct_basis_indices):
            bit_list_alice.append(Alice['randomBits'][i])
            basis_list_alice.append(Alice['randomBases'][i])
            bit_list_bob.append(Bob['measuredBits'][i])
            basis_list_bob.append(Bob['randomBases'][i])
            bit_list_eve.append(Eve['measuredBits'][i])
            basis_list_eve.append(Eve['randomBases'][i])
            bit_list_eve.append(Eva['measuredBits'][i])
            basis_list_eve.append(Eva['randomBases'][i])
            
    return (bit_list_alice, basis_list_alice, bit_list_bob, basis_list_bob, bit_list_eve, basis_list_eve, bit_list_eva, basis_list_eva)      

def etape6_2():
    input = [(0, int(BITSIZE/4)), 
            (int(BITSIZE/4), int(2*BITSIZE/4)), 
            (int(2*BITSIZE/4), int(3*BITSIZE/4)), 
            (int(3*BITSIZE/4), BITSIZE)]
    
    pool = Pool(5)
    
    results = pool.map(etape6_1, input)
    
    temp_bit_list_alice =          results[0][0] + results[1][0] + results[2][0] + results[3][0]
    temp_polarisation_list_alice = results[0][1] + results[1][1] + results[2][1] + results[3][1]
    temp_bit_list_bob =            results[0][2] + results[1][2] + results[2][2] + results[3][2]
    temp_polarisation_list_bob =   results[0][3] + results[1][3] + results[2][3] + results[3][3]
    temp_bit_list_eve =            results[0][4] + results[1][4] + results[2][4] + results[3][4]
    temp_polarisation_list_eve =   results[0][5] + results[1][5] + results[2][5] + results[3][5]
    temp_bit_list_eva =            results[0][6] + results[1][6] + results[2][6] + results[3][6]
    temp_polarisation_list_eva =   results[0][7] + results[1][7] + results[2][7] + results[3][7]
    
    Alice['selectedBits'] = temp_bit_list_alice
    Bob['selectedBits'] = temp_bit_list_bob
    Eve['selectedBits'] = temp_bit_list_eve
    Eva['selectedBits'] = temp_bit_list_eva
    Alice['selectedBases'] = temp_polarisation_list_alice
    Bob['selectedBases'] = temp_polarisation_list_bob
    Eve['selectedBases'] = temp_polarisation_list_eve
    Eva['selectedBases'] = temp_polarisation_list_eva
    
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
    
    print("Les bits et les bases d'eve:")
    print(Eve['measuredBits'])
    print(Eve['randomBases'], "\n")
    
    print("Les bits et les bases d'eva:")
    print(Eva['measuredBits'])
    print(Eva['randomBases'], "\n")
    
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
    print("Bases et bits séléctionnés pour Bob:")
    print(Bob['selectedBits'])
    print(Bob['selectedBases'], "\n")
    print("Percentage de similarité: ", (BITSIZE-len(Alice['selectedBits']))/BITSIZE*100,"%")

if __name__ == "__main__":
            print("Lancez le protocol BB84")
            userInput =  input("Combien de bits voullez vous tester? (Recommendez: petit)\n")
            PresentationBB84(int(userInput))   
        
        
        