import numpy as np
import sys
import random as rnd
from primePy import primes

def write_to_file(fName, textToWrite):
    fOut = open(fName, 'a+')
    fOut.write(textToWrite)
    fOut.close

def read_from_file(fName):
    fIn = open(fName, 'r')
    return fIn.readlines()

def divides_a_b(a,b):
    if b%a == 0:
        return True
    return False

def b36_num_to_digit(num):
    key = '0123456789abcdefghijklmnopqrstuvwxyz'
    if num < 36:
        if num >= 0:
            return key[int(num)]
    
def num_to_b36(n):
    s = ""
    while n > 0:
        s = b36_num_to_digit(n%36) + s
        n -= n%36
        n /= 36
    return s

def b36_to_num(b36str):
    key = '0123456789abcdefghijklmnopqrstuvwxyz'
    s = 0
    exp = 1
    # read b36str in reverse with b36str[::-1]
    for ch in b36str[::-1]:
        num = key.find(ch)
        s += num*exp
        exp *= 36
    return s

def get_random_prime_in_range(lowBound, upBound):
    r = rnd.randint(lowBound, upBound)
    idx = 0
    while not primes.check(r+idx):
        idx += 1
    return r+idx
    
def get_array_of_primes_in_range(numPrimes, lowBound, upBound):
    out = []
    out.append(get_random_prime_in_range(lowBound, upBound))
    while len(out) < numPrimes:
        p = get_random_prime_in_range(lowBound, upBound)
        try:
            out.index(p)
        except ValueError:
            out.append(p)
        else:
            print(p, "is already in the array")
    return out

def make_voter_list(list_file_name, numVoters):
    p_array = get_array_of_primes_in_range(numVoters, 1000000000, 9999999999)
    for p in p_array:
        write_to_file(list_file_name, num_to_b36(p))
        write_to_file(list_file_name, '\n')

def simulate_2_candidate_election(prob_of_candidate, num_voters, lowBound=1000000, upBound=9999999):
    voter_list = get_array_of_primes_in_range(num_voters, lowBound, upBound)
    c1 = 0
    c2 = 0
    while c1 == 0:
        c1 = get_random_prime_in_range(0, lowBound-1)
        try:
            voter_list.index(c1)
        except ValueError:
            print("Candidate 1 key:", c1)
        else:
            print(c1, "is already a voter number")
            c1 = 0
    while c2 == 0:
        c2 = get_random_prime_in_range(0, lowBound-1)
        try:
            voter_list.index(c2)
        except ValueError:
            print("Candidate 2 key:", c2)
        else:
            print(c2, "is already a voter number")
            c2 = 0
    votes = []
    for v in voter_list:
        r = rnd.random()
        if r < prob_of_candidate:
            votes.append(v*c1)
        else:
            votes.append(v*c2)
    return (c1, c2, voter_list, votes)

def tally_2_candidate_election(c1_key, c2_key, votes):
    c1_num_votes = 0
    c2_num_votes = 0
    for v in votes:
        if v % c1_key == 0:
            c1_num_votes += 1
        if v % c2_key == 0:
            c2_num_votes += 1
    print("Number of votes for Candidate 1:", c1_num_votes*100, "  (", c1_num_votes/len(votes), "% )")
    print("Number of votes for Candidate 2:", c2_num_votes*100, "  (", c2_num_votes/len(votes), "% )")
    return (c1_num_votes, c2_num_votes)
    
def check_votes_for_fraud(voter_list, votes):
    exitFlag = False
    for v in voter_list:
        num_votes_cast = 0
        for vt in votes:
            if vt % v == 0:
                num_votes_cast += 1
        if num_votes_cast > 1:
            print("Voter", v, "voted multiple times")
            exitFlag = True
    return exitFlag



if __name__ == '__main__':
    
    lowBound=1000000000
    upBound=5336500537*2
    prob_candidate_A = 0.5
    num_voters = 3
    num_rand_voter_id = 3
    if len(sys.argv) > 1:
        num_voters = int(sys.argv[1])
        
    
        
    print("")
    print("")
    print("")
    print("Running election simulation with", num_voters, "people and voter IDs from", lowBound, "to", upBound)
    print("--------------------------------------------------------")
    print("")
    (c1, c2, v_list, votes) = simulate_2_candidate_election(prob_candidate_A, num_voters, lowBound, upBound)    
    if check_votes_for_fraud(v_list, votes):
        print("Fraud has been detected in the election.")
    else:
        print("No fraud has been detected in the election.")
        
        
    (c1_num_votes, c2_num_votes) = tally_2_candidate_election(c1, c2, votes)
    
    print(num_rand_voter_id, "randomly selected voter IDs:")
    for i in range(num_rand_voter_id):
        idx = rnd.randint(0, num_voters);
        vid = v_list[idx]
        print("\tVoter", i, ":", vid, "\tVoterID:", num_to_b36(vid))
    
    idx = rnd.randint(0, num_voters);
    v = votes[idx]
    v_id = 0
    print("")
    print("randomly selected vote:", v)
    if v%c1 == 0:
        print("voted for candidate A")
        v_id = round(v/c1)
    if v%c2 == 0:
        print("voted for candidate B")
        v_id = round(v/c2)
    
    for i in range(len(v_list)):
        if v_list[i] == v_id:
            print("Voter ", num_to_b36(v_id), "found in voter list.")
            print("Voter number:", v_id)
    
    
    