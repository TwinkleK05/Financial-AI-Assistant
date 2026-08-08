from pipeline import *

from engine.database import get_pending_chunks 


chunks = get_pending_chunks()

print(len(chunks))

print(chunks[0])