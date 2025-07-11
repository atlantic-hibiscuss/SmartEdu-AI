from transformers import AutoTokenizer

def main():
    # Small tokenizer model keeps this demo quick to run.
    model_name = "distilgpt2"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    text = "Explain recursion to a 12-year-old in two sentences."
    print(f"Text: {text}\n")


    # Encode
    enc = tokenizer(text, return_tensors="pt")
    print("Token IDs:", enc["input_ids"])
    print("Attention mask:", enc["attention_mask"])

    # Decode round-trip
    # This lets us confirm the tokenizer can reconstruct readable text.
    decoded = tokenizer.decode(enc["input_ids"][0], skip_special_tokens=True)
    print("Round-trip decoded:", decoded)

if __name__ == "__main__":
    main()
