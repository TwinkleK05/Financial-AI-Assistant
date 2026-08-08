from pipeline import *

from engine.vector_store import load_vector_mapping

mapping = load_vector_mapping()

print(len(mapping))

print(mapping[0])

print(mapping[1])