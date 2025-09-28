import nltk
from nltk.corpus import wordnet as wn
from difflib import get_close_matches
import shutil
import os

# --- Backup original word list ---
if os.path.exists('words.txt'):
    shutil.copyfile('words.txt', 'words_backup.txt')
    print("Backup created: 'words_backup.txt'")
else:
    print("Warning: 'words.txt' not found. Please make sure your word list exists.")

# Download WordNet if needed
nltk.download('wordnet')

# --- Helper functions ---
def get_pos(word):
    if wn.synsets(word, pos=wn.NOUN): return 'noun'
    elif wn.synsets(word, pos=wn.VERB): return 'verb'
    elif wn.synsets(word, pos=wn.ADJ): return 'adjective'
    elif wn.synsets(word, pos=wn.ADV): return 'adverb'
    else: return None

def all_pos(word):
    pos_list = []
    if wn.synsets(word, pos=wn.NOUN): pos_list.append('noun')
    if wn.synsets(word, pos=wn.VERB): pos_list.append('verb')
    if wn.synsets(word, pos=wn.ADJ): pos_list.append('adjective')
    if wn.synsets(word, pos=wn.ADV): pos_list.append('adverb')
    return pos_list if pos_list else ['unknown']

def most_likely_pos(word):
    pos_counts = {
        'noun': len(wn.synsets(word, pos=wn.NOUN)),
        'verb': len(wn.synsets(word, pos=wn.VERB)),
        'adjective': len(wn.synsets(word, pos=wn.ADJ)),
        'adverb': len(wn.synsets(word, pos=wn.ADV))
    }
    pos_counts = {k:v for k,v in pos_counts.items() if v>0}
    if not pos_counts: return None
    return max(pos_counts, key=pos_counts.get)

def assign_word(word, replacement):
    pos_list = all_pos(replacement)
    if len(pos_list) > 1:
        likely_pos = most_likely_pos(replacement)
        if likely_pos:
            if likely_pos == 'noun': nouns.append(replacement)
            elif likely_pos == 'verb': verbs.append(replacement)
            elif likely_pos == 'adjective': adjectives.append(replacement)
            elif likely_pos == 'adverb': adverbs.append(replacement)
            replacements_log.append(f"{word} -> {replacement} ({', '.join(pos_list)}), auto-assigned as {likely_pos}")
        else:
            with open('ambiguous_words.txt','a') as f:
                f.write(f"{word} -> {replacement} ({', '.join(pos_list)})\n")
            print(f"Flagged ambiguous: {word} -> {replacement} ({', '.join(pos_list)})")
    else:
        pos = pos_list[0]
        if pos == 'noun': nouns.append(replacement)
        elif pos == 'verb': verbs.append(replacement)
        elif pos == 'adjective': adjectives.append(replacement)
        elif pos == 'adverb': adverbs.append(replacement)
        replacements_log.append(f"{word} -> {replacement} ({pos})")

def correct_spelling(word, n=5, cutoff=0.7):
    close_matches = get_close_matches(word, lemma_freq.keys(), n=n, cutoff=cutoff)
    if not close_matches: return []
    return sorted(close_matches, key=lambda x: lemma_freq.get(x,0), reverse=True)

# --- Read words ---
with open('words.txt', 'r') as f:
    words = [line.strip() for line in f if line.strip()]

# --- Initialize lists ---
nouns, verbs, adjectives, adverbs, unknown_words = [], [], [], [], []

# --- Categorize known words ---
for word in words:
    pos = get_pos(word)
    if pos == 'noun': nouns.append(word)
    elif pos == 'verb': verbs.append(word)
    elif pos == 'adjective': adjectives.append(word)
    elif pos == 'adverb': adverbs.append(word)
    else: unknown_words.append(word)

# --- Prepare WordNet lemma frequency ---
lemma_freq = {}
for syn in wn.all_synsets():
    for lemma in syn.lemmas():
        lemma_name = lemma.name()
        lemma_freq[lemma_name] = lemma_freq.get(lemma_name, 0) + lemma.count()

# --- Workflow selection ---
print("Choose workflow mode:")
print("1. Safe Automatic Replacement")
print("2. Batch Preview for Ambiguous Words")
print("3. Interactive Mode")
print("4. Final Preview Mode")
print("5. Automatic Top Replacement for All Unknowns")
print("6. Top-N Suggestions for Each Unknown")
mode = input("Enter mode number: ").strip()

replacements_log = []

# --- Unified processing with spell correction ---
for word in unknown_words:
    # --- Spell correction ---
    if not wn.synsets(word):
        suggestions = correct_spelling(word)
        if suggestions:
            replacement = suggestions[0]  # top suggestion
            print(f"Auto-corrected '{word}' -> '{replacement}'")
        else:
            replacement = word
            print(f"No correction found for '{word}'")
    else:
        replacement = word

    # --- Workflow handling ---
    if mode == '1':  # Safe Automatic
        assign_word(word, replacement)
    elif mode == '2':  # Batch Preview
        close = correct_spelling(word)[:5] if replacement==word else [replacement]
        print(f"\nUnknown word: '{word}'")
        for i,s in enumerate(close,1):
            print(f"{i}. {s} ({', '.join(all_pos(s))})")
        print("0. Skip / leave as unknown")
        choice = input("Choose replacement: ").strip()
        if choice.isdigit() and 0 < int(choice) <= len(close):
            assign_word(word, close[int(choice)-1])
    elif mode == '3':  # Interactive
        close = correct_spelling(word)[:5] if replacement==word else [replacement]
        print(f"\nUnknown word: '{word}'")
        for i,s in enumerate(close,1):
            print(f"{i}. {s} ({', '.join(all_pos(s))})")
        print("0. Skip / leave as unknown")
        choice = input("Choose replacement: ").strip()
        if choice.isdigit() and 0 < int(choice) <= len(close):
            assign_word(word, close[int(choice)-1])
    elif mode == '4':  # Final Preview
        close = correct_spelling(word)[:5] if replacement==word else [replacement]
        print(f"\nUnknown word: '{word}'")
        for i,s in enumerate(close,1):
            print(f"{i}. {s} ({', '.join(all_pos(s))})")
        print("0. Skip / leave as unknown")
        choice = input("Choose replacement: ").strip()
        if choice.isdigit() and 0 < int(choice) <= len(close):
            assign_word(word, close[int(choice)-1])
    elif mode == '5':  # Automatic Top Replacement
        assign_word(word, replacement)
    elif mode == '6':  # Top-N Suggestions
        top_n = int(input("Enter number of top suggestions: ").strip())
        close = correct_spelling(word, n=top_n)[:top_n] if replacement==word else [replacement]
        print(f"\nUnknown word: '{word}'")
        for i,s in enumerate(close,1):
            print(f"{i}. {s} ({', '.join(all_pos(s))})")
        print("0. Skip / leave as unknown")
        choice = input("Choose replacement: ").strip()
        if choice.isdigit() and 0 < int(choice) <= len(close):
            assign_word(word, close[int(choice)-1])

# --- Save categorized words ---
with open('nouns.txt','w') as f: f.write('\n'.join(nouns))
with open('verbs.txt','w') as f: f.write('\n'.join(verbs))
with open('adjectives.txt','w') as f: f.write('\n'.join(adjectives))
with open('adverbs.txt','w') as f: f.write('\n'.join(adverbs))

# --- Save replacements log ---
with open('replacements_log.txt','w') as f:
    for line in replacements_log: f.write(line+'\n')

print("\nWorkflow complete!")
print("Check 'replacements_log.txt' for all replacements.")
print("Check 'ambiguous_words.txt' for words with multiple POS flagged for review.")
print("Original word list preserved as 'words_backup.txt'.")
