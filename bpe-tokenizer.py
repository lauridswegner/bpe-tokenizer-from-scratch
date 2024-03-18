# function to get pairs of tokens
def get_pairs(ids):
    counts = {}
    for pair in zip(ids, ids[1:]):
        counts[pair] = counts.get(pair, 0) + 1
    return counts

# function to merge pairs together
def merge(ids, pair, idx):
    # in the list of ints (ids), replace all consecutive 
    # occurences of pair with the new token idx
    newids = []
    i = 0
    while i < len(ids):
        # if we are not at the very last position && the pair matches -> replace it
        if i < len(ids) - 1 and ids[i] == pair[0] and ids[i+1] == pair[1]:
            newids.append(idx)
            i += 2
        else:
            newids.append(ids[i])
            i += 1
    return newids

# read the text into tokens
with open("rots.txt") as file:
    content = file.read()
tokens = content.encode("utf-8")
tokens = list(map(int, tokens))
#print("token length:", len(tokens))

# get pairs from tokens
pairs = get_pairs(tokens)
#print(sorted(((v, k) for k, v in pairs.items()), reverse=True))

# variables for the merge-process
vocab_size = 276 # desired final vocabulary size
num_merges = vocab_size - 256
ids = list(tokens)

# merging processs
merges = {}
for i in range(num_merges):
    pairs = get_pairs(ids)
    pair = max(pairs, key=pairs.get)
    idx = 256 + i
    #print(f"merging {pair} into a new token {idx}")
    ids = merge(ids, pair, idx)
    merges[pair] = idx 

# determine the compression-ratio
print(f"compression ratio: {len(tokens) / len(ids):.2f}X")

# function for decoding
vocab = {idx: bytes([idx]) for idx in range(256)}
for (p0, p1), idx in merges.items():
    vocab[idx] = vocab[p0] + vocab[p1]
def decode(ids):
    # given ids (list of integers), return string
    tokens = b"".join(vocab[idx] for idx in ids)
    text = tokens.decode("utf-8", errors='replace')
    return text

# function for encoding
def encode(text):
    # given a string, return list of integers (the tokens)
    tokens = list(text.encode("utf-8"))
    while len(tokens) >= 2:
        pairs = get_pairs(tokens)
        pair = min(pairs, key=lambda p: merges.get(p, float("inf")))
        if pair not in merges:
            break # nothing else can be merged
        idx = merges[pair]
        tokens = merge(tokens, pair, idx)
    return tokens

print("Do, or do not, there is no try.")
