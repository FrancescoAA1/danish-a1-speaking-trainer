copilot --plan "
I have 20 days to pass a 15-minute Danish A1 speaking exam. I have a PDF book with 13 chapters of phrases, 13 reading exercises, a grammar section, and a glossary.

Build a minimal, practical learning pipeline focused on speaking practice.

1. PDF extractor:
- Extract all spoken phrases from 13 chapters
- Format output as: 'Chapter X: Danish phrase'

2. Reading extraction:
- Extract the 13 reading exercises as separate text blocks

3. Grammar extractor (simple rules only):
Extract ONLY:
- V2 word order rule
- present tense verbs
- modal verbs (kan, vil, skal)
- basic prepositions

Output as a short cheat sheet (no complex NLP)

4. Audio generation:
- Use edge-tts (voice: da-DK-Christel)
- Generate audio for each Danish phrase

5. Anki deck generator:
- Create CSV format:
  Front = Italian prompt / meaning
  Back = Danish phrase
  Include audio file reference/tag

6. CLI speaking practice tool:
- Randomly select a phrase
- Prompt user to speak (5–8 seconds via microphone)
- Transcribe speech using Whisper
- Compare transcription with expected Danish phrase using GPT-4o-mini
- Output simple feedback:
  - correct / incorrect
  - missing words
  - word order mistakes

7. Error logging:
- Track only:
  ['word_order', 'grammar', 'vocab']
- Save errors to JSON file

8. Daily practice script:
- 5 shadowing phrases
- 3 speaking prompts
- 1 error review session

Constraints:
- Use only free tools: edge-tts, whisper, OpenAI GPT-4o-mini
- Keep architecture minimal and modular
- Start with PDF extractor module first
"