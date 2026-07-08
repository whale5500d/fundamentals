"""
A단계 개선 재검증: causal mask 수정 후, 같은 논리적 위치(질문의 마지막 토큰)의
logits이 그 뒤에 무엇이 이어붙든 동일해지는지 확인.

test_causal_mask_leak.py와 동일한 구조이나, 이번에는 "동일해야 한다(PASS)"는
방향으로 assert한다. 수정 전에는 반대로 "다르다는 것"이 문제였다.
"""

import torch
from custom_transformer.transformer_model import TransformerLanguageModel
from custom_transformer.tokenizer.bpe_tokenizer import BPETokenizer
from custom_transformer.scripts.utils.qa_collate import build_qa_training_pair

torch.manual_seed(42)


def load_qa_pairs(path: str) -> list[tuple[str, str]]:
    qa_pairs = []
    with open(path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            parts = line.split('\t')
            if len(parts) != 2:
                continue
            question, answer = parts
            qa_pairs.append((question, answer))
    return qa_pairs


def test_causal_mask_no_longer_leaks_future_info():
    """수정 후, 미래 토큰이 붙어도 과거 위치의 logits이 변하지 않아야 한다"""
    qa_pairs = load_qa_pairs("src/custom_transformer/scripts/raw_data/korean_qa.txt")
    flat_corpus = [q for q, _ in qa_pairs] + [a for _, a in qa_pairs]

    tokenizer = BPETokenizer(vocab_size=300)
    tokenizer.train(flat_corpus)
    vocab_size = len(tokenizer.token_to_id)

    model = TransformerLanguageModel(
        vocab_size=vocab_size, d_model=256, num_heads=8,
        num_layers=4, d_ff=1024, max_len=512, dropout=0.0
    )
    model.eval()

    question, answer = qa_pairs[2]  # '오늘 조깅 할 거야?' -- 수정 전 결함이 관찰됐던 사례
    question_ids = tokenizer.encode(question)
    eos_id = tokenizer.token_to_id[tokenizer.eos_token]
    answer_ids = tokenizer.encode(answer) + [eos_id]

    with torch.no_grad():
        short_input = torch.tensor([question_ids])
        short_logits = model(short_input)[0, -1, :]

        inputs, _ = build_qa_training_pair(question_ids, answer_ids)
        long_input = torch.tensor([inputs])
        long_position = len(question_ids) - 1
        long_logits = model(long_input)[0, long_position, :]

    are_identical = torch.allclose(short_logits, long_logits, atol=1e-5)
    max_diff = torch.max(torch.abs(short_logits - long_logits)).item()

    print(f"두 logits이 동일한가: {are_identical}")
    print(f"최대 절댓값 차이: {max_diff:.8f}")

    assert are_identical, (
        f"수정 후에도 causal mask가 여전히 새고 있음 (최대 차이: {max_diff})"
    )
    print("PASS: causal mask가 정상적으로 미래 토큰을 차단하고 있음을 확인")


if __name__ == "__main__":
    test_causal_mask_no_longer_leaks_future_info()