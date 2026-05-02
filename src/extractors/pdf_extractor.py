"""PDF extractor for Danish A1 phrases from ebook chapters."""

import json
import re
from pathlib import Path
import pdfplumber


def extract_phrases_from_pdf(pdf_path: str, chapter_num: int) -> list:
    """
    Extract Danish phrases from a chapter PDF.
    
    Returns list of dicts: {phrase, english_meaning, chapter}
    """
    phrases = []
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                text = page.extract_text()
                if not text:
                    continue
                
                lines = text.split('\n')
                
                for i, line in enumerate(lines):
                    line = line.strip()
                    if not line:
                        continue
                    
                    # Skip headers, instructions, page numbers
                    if any(skip in line.lower() for skip in 
                           ['kommunikation', 'dialoger', 'klassearbejde', 'brug følgende', 
                            'gå rundt', 'interview', '.indd', 'no writing', 'allowed',
                            'der må ikke', 'univers', 'variationen', 'univers A', 'univers B']):
                        continue
                    
                    # Extract dialogue lines (A: ... or B: ...)
                    if line.startswith('A:') or line.startswith('B:'):
                        # Remove speaker marker
                        phrase = line[2:].strip()
                        
                        # Clean phrase: remove multiple slashes, pipe characters
                        phrase = re.sub(r'\s*[/|]\s*', ' / ', phrase).strip()
                        
                        # Skip if only ellipsis, very short, or contains too many ellipses
                        if phrase and phrase != '…' and len(phrase) > 2 and phrase.count('…') < 3:
                            phrases.append({
                                'chapter': chapter_num,
                                'phrase': phrase,
                                'english_meaning': '',
                                'source': f"Ch{chapter_num}_p{page_num+1}"
                            })
                    
                    # Also extract standalone question/statement lines (starting with -)
                    elif line.startswith('- ') and len(line) > 4:
                        phrase = line[2:].strip()
                        if phrase not in ['…'] and phrase.count('…') < 2:
                            phrases.append({
                                'chapter': chapter_num,
                                'phrase': phrase,
                                'english_meaning': '',
                                'source': f"Ch{chapter_num}_p{page_num+1}"
                            })
    
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
    
    return phrases


def extract_all_chapters(ebook_dir: str = 'ebook', num_chapters: int = 13) -> dict:
    """
    Extract phrases from all chapter PDFs.
    
    Returns dict with chapter numbers as keys, lists of phrases as values.
    """
    ebook_path = Path(ebook_dir)
    all_phrases = {
        'metadata': {
            'total_chapters': num_chapters,
            'extraction_date': str(Path.cwd()),
        },
        'chapters': {}
    }
    
    for ch_num in range(1, num_chapters + 1):
        chapter_dir = ebook_path / f'Chapter{ch_num}'
        if not chapter_dir.exists():
            print(f"Warning: {chapter_dir} not found")
            continue
        
        # Look for PDF files (prefer mundtlig - speaking)
        pdf_files = list(chapter_dir.glob('*.pdf'))
        if not pdf_files:
            print(f"Warning: No PDFs found in {chapter_dir}")
            continue
        
        # Prioritize complete dialogues: Univers_A_B_C, Variationen, then mundtlig
        univers = [p for p in pdf_files if 'univers' in p.name.lower()]
        variationen = [p for p in pdf_files if 'variationen' in p.name.lower()]
        mundtlig = [p for p in pdf_files if 'mundtlig' in p.name.lower()]
        
        target_pdfs = univers + variationen + mundtlig
        target_pdf = target_pdfs[0] if target_pdfs else pdf_files[0]
        
        print(f"Extracting Chapter {ch_num}: {target_pdf.name}")
        phrases = extract_phrases_from_pdf(str(target_pdf), ch_num)
        all_phrases['chapters'][ch_num] = phrases
        print(f"  -> Found {len(phrases)} phrases")
    
    return all_phrases


def save_phrases(phrases_data: dict, output_path: str = 'data/phrases.json'):
    """Save extracted phrases to JSON file."""
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(phrases_data, f, ensure_ascii=False, indent=2)
    print(f"\nSaved to {output_path}")


if __name__ == '__main__':
    # Test on Chapter 1 first
    print("=" * 60)
    print("PDF EXTRACTOR - Chapter 1 Test")
    print("=" * 60)
    
    phrases = extract_phrases_from_pdf('ebook/Chapter1/kap1_mundtlig.pdf', 1)
    print(f"\nExtracted {len(phrases)} phrases from Chapter 1:")
    for i, p in enumerate(phrases[:5], 1):
        print(f"\n{i}. {p['phrase'][:60]}...")
    
    # Full extraction
    print("\n" + "=" * 60)
    print("EXTRACTING ALL CHAPTERS")
    print("=" * 60)
    all_data = extract_all_chapters()
    
    total_phrases = sum(len(p) for p in all_data['chapters'].values())
    print(f"\n[OK] Total phrases extracted: {total_phrases}")
    
    save_phrases(all_data)
