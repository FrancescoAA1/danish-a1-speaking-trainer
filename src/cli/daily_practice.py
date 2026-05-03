"""Daily practice workflow - 30 min structured session."""

import argparse
from datetime import datetime
from src.cli.practice_session import PracticeSession


def run_daily_practice(whisper_model: str = 'base', device: str = 'cpu'):
    """
    Run a structured 30-minute daily practice session:
    - 5 shadowing phrases
    - 3 speaking prompts
    - 1 error review
    """
    
    print("\n" + "=" * 70)
    print("DANISH A1 - DAILY PRACTICE SESSION")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    print("\nToday's goal: ~30 minutes of speaking practice\n")
    
    session = PracticeSession(
        whisper_model=whisper_model,
        device=device
    )
    
    # Phase 1: Shadowing
    print("\n" + "." * 70)
    print("PHASE 1: SHADOWING (5 phrases)")
    print("." * 70)
    print("Listen to native Danish pronunciation, then repeat.")
    input("Press Enter to start...")
    
    try:
        session.shadowing_practice(num_phrases=5)
    except KeyboardInterrupt:
        print("\nSkipping shadowing...")
    
    # Phase 2: Speaking
    print("\n" + "." * 70)
    print("PHASE 2: SPEAKING PRACTICE (3 prompts)")
    print("." * 70)
    print("See English meaning, speak the Danish phrase.")
    input("Press Enter to start...")
    
    try:
        session.speaking_practice(num_prompts=3)
    except KeyboardInterrupt:
        print("\nSkipping speaking practice...")
    
    # Phase 3: Error Review
    print("\n" + "." * 70)
    print("PHASE 3: ERROR REVIEW")
    print("." * 70)
    
    session.error_review()
    
    # Save and summary
    print("\n" + "=" * 70)
    print("SESSION SUMMARY")
    print("=" * 70)
    
    summary = session.error_logger.get_error_summary()
    
    if summary['total_errors'] > 0:
        print(f"\nErrors logged: {summary['total_errors']}")
        if summary['italian_interference_patterns']:
            print("\nWatch out for these Italian interference patterns:")
            for pattern, count in list(summary['italian_interference_patterns'].items())[:3]:
                print(f"  - {pattern}")
    else:
        print("\n✓ Great session! No errors logged.")
    
    # Save
    session.error_logger.save_session()
    
    print(f"\nEnded: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\nKeep practicing! You're making progress!")
    print("=" * 70 + "\n")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Daily Danish A1 speaking practice session'
    )
    parser.add_argument(
        '--model',
        default='base',
        choices=['tiny', 'base', 'small', 'medium', 'large'],
        help='Whisper model size (default: base)'
    )
    parser.add_argument(
        '--device',
        default='cpu',
        choices=['cpu', 'cuda'],
        help='Device to use (default: cpu). Use cuda if you have NVIDIA GPU'
    )
    
    args = parser.parse_args()
    
    try:
        run_daily_practice(whisper_model=args.model, device=args.device)
    except Exception as e:
        print(f"\nError: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure microphone is connected and working")
        print("2. Set OPENAI_API_KEY environment variable")
        print("3. Try: python daily_practice.py --help")
