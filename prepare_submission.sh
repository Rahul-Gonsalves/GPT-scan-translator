#!/bin/bash
# Script to prepare submission files for CSCE 421 HW5

echo "Preparing HW5 submission files..."

# Create submission directory
SUBMIT_DIR="HW5_Rahul_Gonsalves_submission"
rm -rf "$SUBMIT_DIR"
mkdir -p "$SUBMIT_DIR/code"

echo "Copying code files..."
# Copy all necessary code files
cp code/model.py "$SUBMIT_DIR/code/"
cp code/generate.py "$SUBMIT_DIR/code/"
cp code/tokenizer.py "$SUBMIT_DIR/code/"
cp code/train.py "$SUBMIT_DIR/code/"
cp code/trainer.py "$SUBMIT_DIR/code/"
cp code/dataset.py "$SUBMIT_DIR/code/"
cp code/main.py "$SUBMIT_DIR/code/"
cp code/test_model.py "$SUBMIT_DIR/code/"

echo "Copying README..."
cp README.md "$SUBMIT_DIR/"

echo "Creating code ZIP..."
cd "$SUBMIT_DIR"
zip -r "../HW5 Rahul Gonsalves.zip" code/ README.md
cd ..

echo ""
echo "=========================================="
echo "Submission files prepared!"
echo "=========================================="
echo ""
echo "You need to submit TWO files to Canvas:"
echo ""
echo "1. PDF Report: HW5_Rahul_Gonsalves.pdf"
echo "   - Compile the .tex file to PDF"
echo "   - You can use Overleaf or local LaTeX installation"
echo ""
echo "2. Code ZIP: HW5 Rahul Gonsalves.zip"
echo "   - Created and ready in current directory"
echo "   - Contains all code files with implementations"
echo ""
echo "=========================================="
echo "Files to submit:"
echo "  1. HW5_Rahul_Gonsalves.pdf (compile from .tex)"
echo "  2. HW5 Rahul Gonsalves.zip (ready)"
echo "=========================================="
