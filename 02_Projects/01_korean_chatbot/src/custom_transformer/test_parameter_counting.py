from custom_transformer.transformer_model import TransformerLanguageModel

model = TransformerLanguageModel(
    vocab_size=300,   # train.py에서 쓴 값과 동일하게
)

total_params = sum(p.numel() for p in model.parameters())
print(f"전체 파라미터 수: {total_params:,}")

for name, param in model.named_parameters():
    print(f"{name}: {param.numel():,}개")