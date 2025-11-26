# How to Compile LaTeX Report on Overleaf

## Quick Steps

1. Go to https://www.overleaf.com/
2. Log in or create a free account
3. Click "New Project" → "Upload Project"
4. Upload the file: `HW5_Rahul_Gonsalves.tex`
5. Overleaf will automatically compile it
6. Download the PDF by clicking "Download PDF" button (top right)
7. Rename to: `HW5 Rahul Gonsalves.pdf`
8. Submit to Canvas along with the ZIP file

## Alternative: Local Compilation

If you have LaTeX installed on your computer:

```bash
cd /home/rahulgonsalves/CSCE421/HW5
pdflatex HW5_Rahul_Gonsalves.tex
pdflatex HW5_Rahul_Gonsalves.tex  # Run twice for cross-references
```

This will create `HW5_Rahul_Gonsalves.pdf` in the same directory.

## Troubleshooting

If you get errors about missing packages, install them:
- Ubuntu/Debian: `sudo apt install texlive-full`
- macOS: Install MacTeX from https://www.tug.org/mactex/
- Windows: Install MiKTeX from https://miktex.org/

Or just use Overleaf - it has all packages pre-installed!

## What You'll Get

A professional PDF report with:
- Title page
- All theoretical questions with detailed answers
- All programming questions with code and results
- Tables and formatted code listings
- Console outputs
- Analysis and conclusions
- ~15-20 pages total

## Files Ready for Submission

1. **HW5 Rahul Gonsalves.pdf** - Compile from .tex file
2. **HW5 Rahul Gonsalves.zip** - Already created ✓

Both files should be submitted separately to Canvas (not the PDF inside the ZIP).
