from pipeline import *

from engine.database import get_pending_chunks 

chunks = get_pending_chunks()

embeddings = generate_embeddings(chunks)

