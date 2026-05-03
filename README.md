# Danish A1 Speaking Trainer

A practical, AI-powered speaking practice tool for Italian speakers preparing for the Danish A1 exam. Built with **Whisper** (speech transcription), **GPT-4o-mini** (error feedback with Italian-specific interference detection), and **edge-tts** (authentic Danish pronunciation).

**Goal:** 20-day intensive speaking practice with structured daily sessions and targeted chapter mastery.

---

## Features

### ✓ Two Practice Modes (NEW!)

#### 1. **Chapter Practice** (Depth-First Learning)
Master one chapter at a time before moving to the next:
```bash
python main.py --chapter 1
```
- **Shadowing:** Listen to native pronunciation, repeat
- **Speaking:** See English meaning, speak the Danish
- All 164 phrases organized by chapter (Ch1-Ch13)
- Get instant feedback on errors

#### 2. **Daily Mixed Practice** (Breadth-First Review)
30-minute structured session mixing all chapters:
```bash
python main.py --daily
```
- 5 shadowing phrases (random chapters)
- 3 speaking prompts (random chapters)  
- 1 error review (today's mistakes)

### ✓ Comprehensive Content
- **164 Danish phrases** from 13 chapters organized by topic
- **Audio files** in authentic da-DK-ChristelNeural voice
- **Grammar cheatsheet** with V2 word order, present tense, modals, prepositions
- **Anki deck** (CSV) for spaced repetition

### ✓ Italian-Specific Error Detection
Automatically identifies common Italian→Danish transfer errors:
- **Over-pronunciation** (Italian: pronounce all letters, Danish: many silent)
- **Stø errors** (unique Danish prosody, no Italian equivalent)
- **Gender confusion** (Italian has gendered nouns, Danish uses en/et)
- **Verb endings** (Italian -o/-a/-i vs Danish uniform -r/-er)
- **Soft D** (Italian [d] vs Danish [ð] or barely audible)
- **R pronunciation** (Italian rolled [r] vs Danish guttural [ʀ])

### ✓ Error Tracking & Analytics
- Error type classification (vocab, word_order, grammar, pronunciation)
- Italian interference pattern detection
- Corrective feedback per error
- Daily summary & improvement suggestions

---

## Setup

### 1. Clone & Install
```bash
git clone https://github.com/FrancescoAA1/danish-a1-speaking-trainer.git
cd danish-a1-speaking-trainer
pip install -r requirements.txt
```

### 2. Set OpenAI API Key
```bash
export OPENAI_API_KEY="sk-..."  # Your OpenAI API key
```

### 3. First Run (Whisper Download)
```bash
python main.py  # Downloads Whisper 'base' model (~1.4GB, one-time)
```

---

## Usage

### Interactive Menu
```bash
python main.py
```
Choose:
- [1] Chapter Practice (pick chapter 1-13)
- [2] Daily Mixed Practice (30-min session)
- [3] Error Review
- [4] Grammar Cheatsheet
- [5] Exit

### Chapter Practice (Direct)
```bash
python main.py --chapter 1    # Practice Chapter 1 (all 11 phrases)
python main.py --chapter 5    # Practice Chapter 5 (all 11 phrases)
```

### Daily Practice (Direct)
```bash
python main.py --daily                          # CPU (default)
python main.py --daily --device cuda            # GPU (10x faster)
python main.py --daily --model tiny             # Faster but less accurate
```

---

## Recommended Study Plan (20 Days)

### **Days 1-13: Master Each Chapter**
```bash
Day 1:  python main.py --chapter 1   # Greetings & names
Day 2:  python main.py --chapter 2   # Family
Day 3:  python main.py --chapter 3   # Work
...
Day 13: python main.py --chapter 13  # Time & numbers
```

### **Days 14-20: Daily Mixed Review**
```bash
python main.py --daily   # Each day: 5 shadowing + 3 speaking + error review
```

---

## Project Structure

```
danish-a1-speaking-trainer/
├── main.py                        # Entry point
├── src/
│   ├── cli/
│   │   ├── practice_session.py   # Chapter + daily practice
│   │   └── daily_practice.py     # Structured 30-min session
│   └── utils/
│       ├── whisper_handler.py    # Speech recording & transcription
│       ├── gpt_feedback.py       # Error comparison + Italian detection
│       └── error_logger.py       # Error tracking
├── data/
│   ├── phrases.json              # 164 phrases (by chapter)
│   ├── phrases_with_audio.json   # Phrases + audio file refs
│   ├── grammar_cheatsheet.md     # V2, modals, prepositions
│   ├── anki_deck.csv             # Anki import format
│   └── errors.json               # Session logs
└── audio/
    ├── ch01/ (11 phrases)
    ├── ch02/ (12 phrases)
    ...
    └── ch13/ (20 phrases)
```

---

## Chapter Breakdown

| Chapter | Topic | Phrases |
|---------|-------|---------|
| 1 | Greetings & introductions | 11 |
| 2 | Family & relationships | 12 |
| 3 | Work & education | 7 |
| 4 | Hobbies | 4 |
| 5 | Sports & activities | 11 |
| 6 | Food & restaurants | 14 |
| 7 | Shopping | 8 |
| 8 | Travel | 13 |
| 9 | Weather & seasons | 15 |
| 10 | Directions | 16 |
| 11 | Emergency & help | 19 |
| 12 | Health | 14 |
| 13 | Time & numbers | 20 |
| **Total** | | **164** |

---

## Tips for Success

1. **Start with Chapter Practice (Days 1-13)**
   - One chapter = ~1-2 hours focused learning
   - Master core phrases in each topic before mixing

2. **Then do Daily Practice (Days 14-20)**
   - Breadth-first review consolidates learning
   - Random selection forces active recall

3. **Review Your Errors**
   - Italian interference patterns show YOUR weak spots
   - Focus on most-repeated mistakes

4. **Read Grammar Cheatsheet First**
   - V2 word order is critical
   - Modal verbs (kan, vil, skal) are frequent

5. **Speak Clearly**
   - Pause between words
   - Quiet environment (no background noise)

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No microphone | Check connection; test with `python -m sounddevice` |
| OPENAI_API_KEY error | Run: `export OPENAI_API_KEY="sk-..."` |
| Slow model download | Use `--model tiny` for testing (~39MB vs 1.4GB) |
| Inaccurate transcription | Speak clearly; use `--model small` or `--model medium` |

---

## Exam Preparation

This tool covers all A1 topics for the **15-minute speaking exam**:
- ✓ Personal info & greetings
- ✓ Family & relationships  
- ✓ Work & education
- ✓ Daily routines
- ✓ Hobbies & interests
- ✓ Travel & directions
- ✓ Food & shopping
- ✓ Time, numbers, dates
- ✓ Health & emergency phrases

---

Good luck with your Danish A1 exam! 🇩🇰
