"""Interactive CLI practice session."""

import random
import json
from pathlib import Path
from src.utils.whisper_handler import get_transcriber
from src.utils.gpt_feedback import get_comparator
from src.utils.error_logger import get_error_logger


class PracticeSession:
    """Interactive speaking practice session."""
    
    def __init__(self, phrases_json: str = 'data/phrases_with_audio.json',
                 grammar_file: str = 'data/grammar_cheatsheet.md',
                 whisper_model: str = 'base',
                 device: str = 'cpu'):
        """
        Initialize practice session.
        
        Args:
            phrases_json: Path to phrases with audio JSON
            grammar_file: Path to grammar cheatsheet
            whisper_model: Whisper model size (tiny, base, small, medium, large)
            device: 'cuda' or 'cpu'
        """
        self.phrases_json = phrases_json
        self.grammar_file = grammar_file
        self.device = device
        
        print("\nInitializing practice session...")
        self.load_phrases()
        
        self.transcriber = get_transcriber(model_size=whisper_model, device=device)
        self.comparator = get_comparator()
        self.error_logger = get_error_logger()
    
    def load_phrases(self):
        """Load phrases from JSON."""
        with open(self.phrases_json, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.phrases = data.get('phrases', [])
        print(f"Loaded {len(self.phrases)} phrases")
    
    def filter_by_chapter(self, chapter: int = None):
        """
        Filter phrases to a specific chapter.
        
        Args:
            chapter: Chapter number (1-13), or None for all
        
        Returns:
            Filtered list of phrases
        """
        if chapter is None:
            return self.phrases
        
        filtered = [p for p in self.phrases if p.get('chapter') == chapter]
        print(f"Loaded {len(filtered)} phrases from Chapter {chapter}")
        return filtered
    
    def show_menu(self):
        """Display main menu."""
        print("\n" + "=" * 70)
        print("DANISH A1 SPEAKING PRACTICE")
        print("=" * 70)
        print("\n[1] Chapter Practice (choose chapter 1-13)")
        print("[2] Daily Mixed Practice (random chapters)")
        print("[3] Error Review (today's mistakes)")
        print("[4] Grammar Cheatsheet")
        print("[5] Exit")
        print("\nChoice: ", end='')
    
    def shadowing_practice(self, num_phrases: int = 5, chapter: int = None):
        """
        Shadowing: listen to audio, then repeat.
        
        Args:
            num_phrases: Number of phrases to practice
            chapter: Specific chapter (1-13) or None for mixed
        """
        phrases_pool = self.filter_by_chapter(chapter)
        
        if not phrases_pool:
            print("No phrases found for this chapter")
            return
        
        print("\n" + "-" * 70)
        if chapter:
            print(f"SHADOWING PRACTICE - CHAPTER {chapter}")
        else:
            print("SHADOWING PRACTICE - MIXED CHAPTERS")
        print("-" * 70)
        print(f"Listen to {num_phrases} Danish phrases and repeat them.\n")
        
        selected = random.sample(phrases_pool, min(num_phrases, len(phrases_pool)))
        
        for i, phrase_data in enumerate(selected, 1):
            phrase = phrase_data.get('phrase', '')
            audio_file = phrase_data.get('audio_file', '')
            
            print(f"\n[{i}/{num_phrases}] {phrase}")
            
            if audio_file and Path(f'audio/{audio_file}').exists():
                print(f"Playing audio: audio/{audio_file}")
                # In a real implementation, would play audio with playsound or similar
                print("(Audio playing...)")
            else:
                print("(Audio not available)")
            
            print("\nSpeak the phrase now (you will have 8 seconds)")
            transcription = self.transcriber.record_and_transcribe(duration=8, language='da')
            print(f"You said: {transcription}")
            
            # Compare
            result = self.comparator.compare_phrases(transcription, phrase)
            
            if result.get('is_correct'):
                print("✓ CORRECT! Well done!")
            else:
                print(f"x Not quite. Try: {phrase}")
                print(f"Feedback: {result.get('feedback', '')}")
    
    def speaking_practice(self, num_prompts: int = 3, chapter: int = None):
        """
        Speaking: user sees English meaning, speaks Danish.
        
        Args:
            num_prompts: Number of speaking prompts
            chapter: Specific chapter (1-13) or None for mixed
        """
        phrases_pool = self.filter_by_chapter(chapter)
        
        if not phrases_pool:
            print("No phrases found for this chapter")
            return
        
        print("\n" + "-" * 70)
        if chapter:
            print(f"SPEAKING PRACTICE - CHAPTER {chapter}")
        else:
            print("SPEAKING PRACTICE - MIXED CHAPTERS")
        print("-" * 70)
        print(f"You will see the English meaning. Speak the Danish phrase.\n")
        
        selected = random.sample(phrases_pool, min(num_prompts, len(phrases_pool)))
        correct = 0
        
        for i, phrase_data in enumerate(selected, 1):
            phrase = phrase_data.get('phrase', '')
            english = phrase_data.get('english_meaning', phrase[:40])
            
            print(f"\n[{i}/{num_prompts}] English: {english}")
            print("Danish phrase? (8 seconds to speak)")
            
            transcription = self.transcriber.record_and_transcribe(duration=8, language='da')
            print(f"You said: {transcription}")
            
            # Compare
            result = self.comparator.compare_phrases(transcription, phrase)
            
            if result.get('is_correct'):
                print("✓ CORRECT!")
                correct += 1
            else:
                print(f"x Expected: {phrase}")
                print(f"Error type: {result.get('error_type', 'unknown')}")
                
                if result.get('italian_interference'):
                    print(f"Italian interference: {result['italian_interference']}")
                
                print(f"Feedback: {result.get('feedback', '')}")
                
                # Log error
                self.error_logger.log_error(
                    phrase=phrase,
                    user_transcription=transcription,
                    expected_phrase=phrase,
                    error_type=result.get('error_type', 'unknown'),
                    italian_interference=result.get('italian_interference'),
                    feedback=result.get('feedback')
                )
        
        print(f"\n✓ Score: {correct}/{num_prompts} correct")
    
    def error_review(self):
        """Show today's errors and patterns."""
        print("\n" + "-" * 70)
        print("ERROR REVIEW")
        print("-" * 70)
        
        summary = self.error_logger.get_error_summary()
        
        print(f"\nTotal errors today: {summary['total_errors']}")
        
        if summary['error_types']:
            print("\nError breakdown:")
            for error_type, count in sorted(summary['error_types'].items(), 
                                           key=lambda x: x[1], reverse=True):
                print(f"  - {error_type}: {count}")
        
        if summary['italian_interference_patterns']:
            print("\nItalian interference patterns:")
            for pattern, count in sorted(summary['italian_interference_patterns'].items(),
                                        key=lambda x: x[1], reverse=True):
                print(f"  - {pattern}: {count} occurrences")
        
        if summary['top_mistakes']:
            print("\nTop mistakes to focus on:")
            for phrase, count in summary['top_mistakes'].items():
                print(f"  - {phrase} ({count} times)")
    
    def show_grammar(self):
        """Display grammar cheatsheet."""
        print("\n" + "-" * 70)
        print("GRAMMAR CHEATSHEET")
        print("-" * 70)
        
        try:
            with open(self.grammar_file, 'r', encoding='utf-8') as f:
                content = f.read()
            print(content)
        except Exception as e:
            print(f"Could not load grammar file: {e}")
    
    def run(self):
        """Run the interactive practice session."""
        while True:
            self.show_menu()
            
            try:
                choice = input().strip()
            except EOFError:
                print("\nExiting...")
                break
            
            if choice == '1':
                self.chapter_practice()
            elif choice == '2':
                self.daily_mixed_practice()
            elif choice == '3':
                self.error_review()
            elif choice == '4':
                self.show_grammar()
            elif choice == '5':
                print("\nSaving session...")
                self.error_logger.save_session()
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")
    
    def chapter_practice(self):
        """Practice a specific chapter."""
        print("\n" + "-" * 70)
        print("CHAPTER PRACTICE")
        print("-" * 70)
        print("Choose a chapter to practice (1-13): ", end='')
        
        try:
            chapter = int(input().strip())
            if chapter < 1 or chapter > 13:
                print("Invalid chapter. Please choose 1-13")
                return
        except ValueError:
            print("Invalid input")
            return
        
        # Get chapter phrases
        chapter_phrases = self.filter_by_chapter(chapter)
        if not chapter_phrases:
            print(f"No phrases found for Chapter {chapter}")
            return
        
        print(f"\nChapter {chapter} has {len(chapter_phrases)} phrases")
        print("\nWhat would you like to practice?")
        print("[1] Shadowing (listen & repeat)")
        print("[2] Speaking (translate from English)")
        print("[3] Both (5 shadowing + 3 speaking)")
        print("Choice: ", end='')
        
        try:
            mode = input().strip()
        except EOFError:
            return
        
        if mode == '1':
            self.shadowing_practice(num_phrases=len(chapter_phrases), chapter=chapter)
        elif mode == '2':
            self.speaking_practice(num_prompts=min(3, len(chapter_phrases)), chapter=chapter)
        elif mode == '3':
            self.shadowing_practice(num_phrases=min(5, len(chapter_phrases)), chapter=chapter)
            self.speaking_practice(num_prompts=min(3, len(chapter_phrases)), chapter=chapter)
        else:
            print("Invalid choice")
    
    def daily_mixed_practice(self):
        """Run daily practice with mixed chapters."""
        print("\n" + "-" * 70)
        print("DAILY MIXED PRACTICE")
        print("-" * 70)
        print("Today: 5 shadowing + 3 speaking from random chapters\n")
        
        self.shadowing_practice(num_phrases=5, chapter=None)
        self.speaking_practice(num_prompts=3, chapter=None)


if __name__ == '__main__':
    print("=" * 70)
    print("DANISH A1 SPEAKING PRACTICE")
    print("=" * 70)
    
    session = PracticeSession(
        whisper_model='base',
        device='cpu'
    )
    
    try:
        session.run()
    except KeyboardInterrupt:
        print("\n\nSession interrupted")
        session.error_logger.save_session()
