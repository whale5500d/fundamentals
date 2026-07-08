"""
causal mask(인과 마스크) 결함 가설 검증.

가설:
    질문의 마지막 토큰 위치가 만들어내는 logits(다음 토큰 예측 확률 분포)는,
    그 뒤에 어떤 토큰이 이어붙든(혹은 아예 없든) 동일해야 한다. 이게 causal
    구조(자기 자신과 그 이전만 참조 가능)의 정의다.

검증 방법:
    같은 질문에 대해, (1) 질문만 있는 입력과 (2) 질문+정답 일부가 이어붙은
    입력을 각각 모델에 통과시켜서, "질문의 마지막 토큰 위치"의 logits이
    두 경우에 정확히 같은지 비교한다. 다르다면 causal mask가 깨져서
    미래 토큰 정보가 새고 있다는 뜻이다.
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


def main():
    qa_pairs = load_qa_pairs("src/custom_transformer/scripts/raw_data/korean_qa.txt")
    flat_corpus = [q for q, _ in qa_pairs] + [a for _, a in qa_pairs]

    tokenizer = BPETokenizer(vocab_size=300)
    tokenizer.train(flat_corpus)
    vocab_size = len(tokenizer.token_to_id)

    # 학습 없이, 무작위 초기화 상태 그대로 확인한다.
    # (causal mask 구조 자체의 결함이라면, 학습 여부와 무관하게 나타나야 한다.
    #  오히려 학습 전에 확인하는 게 "우연히 학습으로 맞춰진 값"이라는 다른
    #  가능성을 배제할 수 있어 더 순수한 검증이다.)
    model = TransformerLanguageModel(
        vocab_size=vocab_size, d_model=256, num_heads=8,
        num_layers=4, d_ff=1024, max_len=512, dropout=0.0  # dropout도 0으로 고정해 무작위성 배제
    )
    model.eval()

    print("=== causal mask 결함 검증 (학습 전, 무작위 초기화 상태) ===\n")

    question, answer = qa_pairs[2]  # '오늘 조깅 할 거야?' - 실제로 불일치가 관찰된 사례
    print(f"검증 대상 질문: {question!r}\n")

    question_ids = tokenizer.encode(question)
    eos_id = tokenizer.token_to_id[tokenizer.eos_token]
    answer_ids = tokenizer.encode(answer) + [eos_id]

    with torch.no_grad():
        # (1) 질문만 있는 입력
        short_input = torch.tensor([question_ids])
        short_logits = model(short_input)[0, -1, :]  # 질문 마지막 위치의 logits

        # (2) 질문 + 정답 일부가 이어붙은 입력 (build_qa_training_pair와 동일한 구성)
        inputs, _ = build_qa_training_pair(question_ids, answer_ids)
        long_input = torch.tensor([inputs])
        long_position = len(question_ids) - 1  # 같은 논리적 위치 (질문 마지막 토큰)
        long_logits = model(long_input)[0, long_position, :]

    are_identical = torch.allclose(short_logits, long_logits, atol=1e-6)
    max_diff = torch.max(torch.abs(short_logits - long_logits)).item()

    print(f"(1) 질문만 입력했을 때, 질문 마지막 위치의 logits 앞 5개: {short_logits[:5].tolist()}")
    print(f"(2) 질문+정답 이어붙였을 때, 같은 위치의 logits 앞 5개: {long_logits[:5].tolist()}")
    print()
    print(f"두 logits이 완전히 동일한가: {are_identical}")
    print(f"최대 절댓값 차이: {max_diff:.8f}")

    if not are_identical:
        print("\n[결론] causal mask가 깨져 있습니다. 같은 논리적 위치(질문의 마지막 토큰)인데도,")
        print("뒤에 어떤 토큰이 이어붙는지에 따라 출력이 달라집니다.")
        print("이는 모델이 미래 토큰 정보를 참조하고 있다는 뜻이며,")
        print("scaled_dot_product_attention.py 또는 decoder_layer.py의 mask 처리를 확인해야 합니다.")
    else:
        print("\n[결론] causal mask는 정상입니다. 두 경우의 logits이 동일하므로,")
        print("이전 관찰된 불일치는 다른 원인(예: 학습 과정 자체의 문제)에서 비롯된 것입니다.")


if __name__ == "__main__":
    main()