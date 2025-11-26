#!/usr/bin/env python3
"""
Script to test a trained GPT model and compute test accuracy
"""
import argparse
import torch
from datasets import load_dataset
from model import GPT, GPTConfig
from tokenizer import build_tokenizer
from generate import generate_sample
from tqdm import tqdm

def test_model(args):
    # Load dataset
    data_SCAN = load_dataset("scan", args.data_split, trust_remote_code=True)
    
    # Load tokenizer
    max_len = args.max_len
    tokenizer, vocab_size = build_tokenizer(args, data_SCAN, max_len, args.output_tokenizer_dir)
    
    # Load model
    mconf = GPTConfig(vocab_size, max_len,
                      n_layer=args.n_layer, n_head=args.n_head, n_embd=args.n_embd,
                      isconditional=True)
    
    print("Loading model from:", args.ckpt_path)
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    model = GPT(mconf)
    checkpoint = torch.load(args.ckpt_path, map_location=device)
    model.load_state_dict(checkpoint['model_state_dict'], strict=True)
    model.to(device)
    model.eval()
    
    print(f'Total params: {sum(p.numel() for p in model.parameters())}')
    
    # Test on test set
    test_data = data_SCAN['test']
    correct_count = 0
    total_count = len(test_data)
    
    print(f"\nTesting on {total_count} examples...")
    pbar = tqdm(enumerate(test_data), total=total_count)
    
    for i, data in pbar:
        try:
            generated_actions = generate_sample(model, tokenizer, data['commands'], max_len)
            if generated_actions == data['actions']:
                correct_count += 1
        except Exception as e:
            print(f"\nError on example {i}: {e}")
            continue
        
        if i % 100 == 0:
            pbar.set_description(f'Accuracy: {correct_count / (i + 1):.4f}')
    
    accuracy = correct_count / total_count
    print(f'\n{"="*60}')
    print(f'Final Test Accuracy: {accuracy:.4f} ({correct_count}/{total_count})')
    print(f'{"="*60}')
    
    # Show some examples
    print("\nSample predictions:")
    for i in range(min(5, total_count)):
        generated = generate_sample(model, tokenizer, test_data[i]['commands'], max_len)
        correct = "✓" if generated == test_data[i]['actions'] else "✗"
        print(f"\n{correct} Example {i+1}:")
        print(f"  Command:  {test_data[i]['commands']}")
        print(f"  Expected: {test_data[i]['actions']}")
        print(f"  Got:      {generated}")
    
    return accuracy

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--ckpt_path', type=str, required=True,
                        help="Path to model checkpoint")
    parser.add_argument('--data_split', type=str, default='simple',
                        help="data split of SCAN dataset")
    parser.add_argument('--n_layer', type=int, default=2,
                        help="number of layers")
    parser.add_argument('--n_head', type=int, default=2,
                        help="number of heads")
    parser.add_argument('--n_embd', type=int, default=16,
                        help="embedding dimension")
    parser.add_argument('--max_len', type=int, default=128,
                        help="max_len")
    parser.add_argument('--output_tokenizer_dir',
                        default='./tokenizer',
                        help="Path to the saved tokenizer directory")
    parser.add_argument('--task', type=str, default='generate',
                        help="Task type (for tokenizer loading)")
    
    args = parser.parse_args()
    test_model(args)
