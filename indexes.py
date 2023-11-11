#https://www.learndatasci.com/glossary/jaccard-similarity/
#https://en.wikipedia.org/wiki/S%C3%B8rensen%E2%80%93Dice_coefficient
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

def jaccard_pair(A,B):
    A_B = list(set(A+B))
    A_value = [1 if species in A else 0 for species in A_B]
    B_value = [1 if species in B else 0 for species in A_B]
    print("jaccard: ", jaccard_binary(A_value, B_value))

def chekanovsky_pair(A,B):
    print("chekanovsky: ",(2*len(set(A).intersection(set(B)))) / (len(A) + len(B)))

A = list(map(str.lower, Path('./species/canada_alaska').read_text().split('\n')))
A = list(map(str.strip, A))
B = list(map(str.lower, Path( './species/ne_europe').read_text().split('\n')))
B = list(map(str.strip, B))
C = list(map(str.lower, Path('./species/russia_ws').read_text().split('\n')))
C = list(map(str.strip, C))

print('canada_alaska-ne_europe')
jaccard_pair(A,B)
chekanovsky_pair(A,B)
print('canada_alaska-russia_ws')
jaccard_pair(A,C)
chekanovsky_pair(A,C)
print('ne_europe-russia_ws')
jaccard_pair(B,C)
chekanovsky_pair(B,C)