import torch
from datasets import load_dataset
from tqdm import tqdm

from model import GPT, GPTConfig
from tokenizer import build_tokenizer

from torch.nn import functional as F


def load_model(model_path, config):
    model = GPT(config)
    checkpoint = torch.load(model_path, map_location='cpu')
    model.load_state_dict(checkpoint['model_state_dict'], strict=True)
    model.eval()
    return model


def sample_from_logits(logits, temp=1.0):
    # logits = top_k_logits(logits, top_k)
    probabilities = F.softmax(logits / temp, dim=-1)
    next_token = torch.multinomial(probabilities, 1, replacement=True)
    return next_token


def generate_sample(model, tokenizer, conditions, max_length):
    model.eval()
    device = next(model.parameters()).device
    input_ids = tokenizer.generation_encode(conditions)
    input_ids = torch.tensor([input_ids], dtype=torch.long).to(device)
    len_conditions = len(input_ids[0])

    with torch.no_grad():
        for _ in range(max_length - len_conditions):

            # Generate one token at a time, and append it to the input to do generation iteratively until </s> is generated
            # hint: use the "sample_from_logits" function to sample the next token based on model's output (logits)
            ### YOUR CODE HERE ###
            # Forward pass through the model
            logits, _, _ = model(input_ids)
            
            # Get logits for the last token in the sequence
            last_logits = logits[0, -1, :]
            
            # Sample the next token from the logits
            next_token = sample_from_logits(last_logits, temp=1.0)
            
            # Append the next token to the input sequence
            input_ids = torch.cat([input_ids, next_token.unsqueeze(0)], dim=1)

            # hint: uncomment the following finishing conditions
            if next_token.item() == tokenizer.vocab["</s>"] or next_token.item() == tokenizer.vocab["<pad>"]:
                break
            ### END YOUR CODE ###


    generated_text = tokenizer.decode(input_ids[0][len_conditions:])
    return generated_text


def generate(args):

    data_SCAN = load_dataset("scan", args.data_split, trust_remote_code=True)

    max_len = args.max_len
    tokenizer, vocab_size = build_tokenizer(args, data_SCAN, max_len, args.output_tokenizer_dir)

    mconf = GPTConfig(vocab_size, max_len,
                      n_layer=args.n_layer, n_head=args.n_head, n_embd=args.n_embd,
                      isconditional=True)

    # Load model and tokenizer
    print("loading model")
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    model = load_model(args.ckpt_path, mconf).to(device)
    print('total params:', sum(p.numel() for p in model.parameters()))


    # Sample generation
    test_data = data_SCAN['test']
    correct_count = 0
    pbar = tqdm(enumerate(test_data), total=len(test_data))
    for i, data in pbar:
        generated_actions = generate_sample(model, tokenizer, data['commands'], max_len)
        if generated_actions == data['actions']:
            correct_count += 1
        pbar.set_description(f'Accuracy: {correct_count / (i + 1):.4f}')
    print(f'Test accuracy: {correct_count / len(test_data)}')
