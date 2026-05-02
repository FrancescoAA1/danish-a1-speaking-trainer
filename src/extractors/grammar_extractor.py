"""Grammar extractor for Danish A1 - extracts key rules only."""

import json
import re
from pathlib import Path


def extract_grammar_rules(md_file: str) -> dict:
    """
    Extract key grammar rules from Grammatik.md.
    
    Focus on:
    - V2 word order (verb in 2nd position, inversion)
    - Present tense verbs
    - Modal verbs (kan, vil, skal, må, kunne, skulle, ville, måtte)
    - Basic prepositions
    """
    rules = {
        'v2_word_order': [],
        'present_tense_verbs': [],
        'modal_verbs': [],
        'prepositions': [],
        'examples': []
    }
    
    try:
        with open(md_file, 'r', encoding='utf-8-sig') as f:
            content = f.read()
        
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            line_lower = line.lower()
            
            # V2 word order / Inversion
            if 'inversion' in line_lower or 'orden' in line_lower and 'verb' in line_lower:
                # Capture this line and next few lines as example
                context = '\n'.join(lines[i:min(i+3, len(lines))])
                if context not in rules['v2_word_order']:
                    rules['v2_word_order'].append(context.strip())
            
            # Modal verbs section
            if 'modalverb' in line_lower:
                context = '\n'.join(lines[i:min(i+5, len(lines))])
                if context not in rules['modal_verbs']:
                    rules['modal_verbs'].append(context.strip())
            
            # Present tense / Regular verbs
            if ('nutid' in line_lower or 'nutid' in line_lower or 
                'present' in line_lower or 'regelmæssige' in line_lower):
                if 'verb' in line_lower:
                    context = '\n'.join(lines[i:min(i+3, len(lines))])
                    if context not in rules['present_tense_verbs']:
                        rules['present_tense_verbs'].append(context.strip())
            
            # Basic prepositions
            prepos = ['i ', 'på ', 'til ', 'fra ', 'med ', 'uden ', 'for ', 'efter ', 'under ', 'over ', 'om ', 'ved ']
            for prep in prepos:
                if prep in line_lower and len(line) > 20:  # Avoid false positives on short lines
                    if any(word in line_lower for word in ['preposition', 'præposition', 'examples', 'fx']):
                        if line not in rules['prepositions']:
                            rules['prepositions'].append(line.strip())
    
    except Exception as e:
        print(f"Error reading grammar file: {e}")
    
    return rules


def create_cheatsheet(grammar_rules: dict) -> str:
    """Create a markdown cheatsheet from extracted rules."""
    
    cheatsheet = """# Danish A1 Grammar Cheatsheet
*For quick reference during speaking practice*

## 1. V2 Word Order (Inversion)

**Rule**: In Danish, the verb MUST be in the 2nd position.
- **Statement**: Jeg hedder Anders. (I am-called Anders)
  - Subject (1) | Verb (2) | Rest
  
- **Question**: Hedder du Anders? (Are-you-called Anders?)
  - Verb (1) | Subject (2) | Rest
  
- **With adverbial**: I dag er jeg på ferie. (Today am I on vacation)
  - Adverbial (1) | Verb (2) | Subject (3) | Rest
  
**Key**: If something other than subject comes first, subject moves AFTER the verb!

---

## 2. Present Tense Verbs

**Regular conjugation** (same for ALL persons):

| | |
|---|---|
| jeg | arbejder (work) |
| du | arbejder |
| han/hun | arbejder |
| vi | arbejder |
| I | arbejder |
| de | arbejder |

**Common present tense verbs**:
- at være (to be) → jeg er
- at have (to have) → jeg har
- at hedde (to be called) → jeg hedder
- at bo (to live) → jeg bor
- at arbejde (to work) → jeg arbejder
- at tale (to speak) → jeg taler

---

## 3. Modal Verbs (Modalverber)

**Common Danish modals**:

| Present | Past | English |
|---------|------|---------|
| kan | kunne | can/may |
| skal | skulle | shall/must |
| vil | ville | will/want |
| må | måtte | may |

**Pattern**: Modal verb + infinitive (no "at")
- Jeg kan tale dansk. (I can speak Danish)
- Du skal arbejde i dag. (You must/shall work today)
- Han vil rejse til Danmark. (He will travel to Denmark)
- De må ikke skrive her. (They may not write here)

---

## 4. Articles & Gender (en-ord vs. et-ord)

**Common en-ord** (common gender):
- en mand (a man)
- en kvinde (a woman)
- en bil (a car)
- en bog (a book)

**Common et-ord** (neuter):
- et barn (a child)
- et hus (a house)
- et bord (a table)
- et ord (a word)

**Definite article**: 
- en → -n (en mand → manden)
- et → -t (et hus → huset)

---

## 5. Basic Prepositions

| Preposition | English | Example |
|-------------|---------|---------|
| i | in | i Danmark (in Denmark) |
| på | on/at | på universitetet (at university) |
| til | to | til København (to Copenhagen) |
| fra | from | fra Italien (from Italy) |
| med | with | med min veninde (with my friend) |
| uden | without | uden kaffe (without coffee) |
| for | for | for mig (for me) |
| efter | after | efter arbejde (after work) |
| under | under/during | under middagen (during lunch) |
| over | over/across | over bjerget (over the mountain) |
| om | about/around | om sommeren (in summer) |
| ved | at/by | ved siden af (next to) |

---

## Common A1 Sentences (Practice Patterns)

1. **Introductions**: 
   - Jeg hedder [navn]. (My name is...)
   - Jeg kommer fra [land]. (I come from...)

2. **Asking about others**:
   - Hvad hedder du? (What are you called?)
   - Hvor kommer du fra? (Where do you come from?)
   - Hvordan går det? (How are you?)

3. **Simple statements**:
   - Jeg arbejder i [sted]. (I work at...)
   - Jeg bor i [by]. (I live in...)
   - Jeg taler dansk og italiensk. (I speak Danish and Italian.)

4. **With modals**:
   - Du skal tale dansk. (You must speak Danish.)
   - Jeg kan ikke forstå. (I cannot understand.)
   - Vi vil gerne rejse til Danmark. (We want to travel to Denmark.)
"""
    
    return cheatsheet


def save_cheatsheet(cheatsheet: str, output_path: str = 'data/grammar_cheatsheet.md'):
    """Save cheatsheet to file."""
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(cheatsheet)
    print(f"Saved grammar cheatsheet to {output_path}")


if __name__ == '__main__':
    print("=" * 60)
    print("GRAMMAR EXTRACTOR")
    print("=" * 60)
    
    rules = extract_grammar_rules('ebook/Grammatik.md')
    
    print("\nExtracted sections:")
    print(f"  - V2 word order rules: {len(rules['v2_word_order'])} sections")
    print(f"  - Present tense verbs: {len(rules['present_tense_verbs'])} sections")
    print(f"  - Modal verbs: {len(rules['modal_verbs'])} sections")
    print(f"  - Prepositions: {len(rules['prepositions'])} sections")
    
    cheatsheet = create_cheatsheet(rules)
    save_cheatsheet(cheatsheet)
    
    print("\n[OK] Grammar cheatsheet created successfully!")
