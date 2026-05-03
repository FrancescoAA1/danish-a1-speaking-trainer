#!/usr/bin/env python3
"""
Danish A1 Speaking Trainer - Main entry point.

Two modes:
1. Chapter Practice: Master one chapter at a time (depth-first)
2. Daily Practice: Mixed chapters for comprehensive review (breadth-first)
"""

import os
import sys

# Must be set BEFORE importing packages that depend on Numba
# (Windows workaround for security policies blocking DLLs)
os.environ['NUMBA_DISABLE_JIT'] = '1'

import argparse
from src.cli.practice_session import PracticeSession
from src.cli.daily_practice import run_daily_practice


def main():
    """Main entry point with mode selection."""
    parser = argparse.ArgumentParser(
        description='Danish A1 Speaking Trainer',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                    # Interactive menu
  python main.py --chapter 1        # Practice Chapter 1 only
  python main.py --daily            # Run 30-min daily session
  python main.py --daily --model base --device cuda
        """
    )
    
    parser.add_argument(
        '--chapter',
        type=int,
        metavar='N',
        help='Practice specific chapter (1-13)'
    )
    
    parser.add_argument(
        '--daily',
        action='store_true',
        help='Run 30-minute daily practice with mixed chapters'
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
        help='Device for Whisper (default: cpu). Use cuda with NVIDIA GPU'
    )
    
    args = parser.parse_args()
    
    try:
        if args.daily:
            # Run structured daily session
            run_daily_practice(whisper_model=args.model, device=args.device)
        else:
            # Interactive session
            session = PracticeSession(
                whisper_model=args.model,
                device=args.device
            )
            
            if args.chapter:
                # Jump directly to chapter practice
                if args.chapter < 1 or args.chapter > 13:
                    print(f"Error: Chapter must be 1-13, got {args.chapter}")
                    sys.exit(1)
                
                chapter_phrases = session.filter_by_chapter(args.chapter)
                print(f"\nPracticing Chapter {args.chapter} ({len(chapter_phrases)} phrases)")
                session.shadowing_practice(num_phrases=min(5, len(chapter_phrases)), chapter=args.chapter)
                session.speaking_practice(num_prompts=min(3, len(chapter_phrases)), chapter=args.chapter)
                session.error_logger.save_session()
            else:
                # Interactive menu
                session.run()
    
    except KeyboardInterrupt:
        print("\n\nSession interrupted")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure microphone is connected")
        print("2. Set OPENAI_API_KEY: export OPENAI_API_KEY='your-key'")
        print("3. Try: python main.py --help")
        sys.exit(1)


if __name__ == '__main__':
    main()
