# 📝 Word List Cleaner & POS Categorizer

![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-beta-orange)

A Python toolkit to clean, correct, and categorize word lists. Automatically detects typos, applies corrections, and classifies words into nouns, verbs, adjectives, and adverbs using WordNet. Ambiguous words are intelligently handled, and your original data is always safe.

---

## 🎬 Demo

![Workflow Demo](demo.gif)

### Screenshots

**Workflow Menu**  
![Workflow Menu](docs/workflow_menu.png)  

**Interactive Correction**  
![Interactive Correction](docs/interactive_correction.png)  

**Categorized Outputs**  
![Outputs Preview](docs/outputs_preview.png)  

**Replacement Log Preview**  
![Replacement Log](docs/replacements_log_preview.png)

---

## ⚙️ Usage

1. Place your word list as `words.txt` (one word per line) in the project root.  
2. Run the script:

```bash
python wordlist_cleaner.py
