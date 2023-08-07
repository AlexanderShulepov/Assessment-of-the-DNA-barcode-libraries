#https://www.learndatasci.com/glossary/jaccard-similarity/
import numpy as np
from pathlib import Path

def jaccard_set(list1, list2):
    """Define Jaccard Similarity function for two sets"""
    intersection = len(list(set(list1).intersection(list2)))
    union = (len(list1) + len(list2)) - intersection
    return float(intersection) / union

def jaccard_binary(x,y):
    """A function for finding the similarity between two binary vectors"""
    intersection = np.logical_and(x, y)
    union = np.logical_or(x, y)
    similarity = intersection.sum() / float(union.sum())
    return similarity

def jaccar_pair(A,B):
    A_B = list(set(A+B))
    A_value = [1 if species in A else 0 for species in A_B]
    B_value = [1 if species in B else 0 for species in A_B]

    print(jaccard_binary(A_value, B_value))
    
A = list(map(str.lower, Path('./species/russia_ws').read_text().split('\n')))
A = list(map(str.strip, A))
B = list(map(str.lower, Path('./species/canada_alaska').read_text().split('\n')))
B = list(map(str.strip, B))
C = list(map(str.lower, Path('./species/ne_europe').read_text().split('\n')))
C = list(map(str.strip, C))



print('russia-canada_alaska')
jaccar_pair(A,B)
print('russia-europe_ne')
jaccar_pair(A,C)
print('canada_alaska-europe_ne')
jaccar_pair(B,C)