# function to get pairs of tokens
def get_pairs(ids):
    counts = {}
    for pair in zip(ids, ids[1:]):
        counts[pair] = counts.get(pair, 0) + 1
    return counts


# read the text into tokens
with open("rots.txt") as file:
    content = file.read()
tokens = content.encode("utf-8")
tokens = list(map(int, tokens))

print("token length:", len(tokens))

pairs = get_pairs(tokens)
print(sorted(((v, k) for k, v in pairs.items()), reverse=True))
