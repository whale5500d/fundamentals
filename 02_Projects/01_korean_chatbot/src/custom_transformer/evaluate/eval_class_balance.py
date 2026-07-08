"""
B단계(클래스 불균형) 진단 스크립트.

검증 항목:
    1. korean_qa.txt의 답변이 실제로 "응" / "아니" 로 얼마나 나뉘는지 정확히 집계
    2. 학습 후, 훈련 데이터에 없던 새로운 질문(비슷한 구조, 다른 명사 조합)에 대해
       greedy decoding(확률이 가장 높은 토큰만 뽑는 방식, 샘플링 무작위성 배제)으로
       첫 토큰을 확인했을 때, "아니"가 정답이어야 할 상황에서도 "응"으로
       편향되는지 확인

주의:
    train.py의 generate()는 temperature/top_k로 확률적 샘플링을 하므로,
    "편향 자체"를 순수하게 보려면 확률적 요소를 배제한 greedy decoding
    (가장 확률 높은 토큰만 선택)으로 진단해야 한다.
"""

import torch
from custom_transformer.transformer_model import TransformerLanguageModel
from custom_transformer.tokenizer.bpe_tokenizer import BPETokenizer
from custom_transformer.scripts.utils.qa_collate import build_qa_training_pair, IGNORE_INDEX
import torch.nn as nn
import torch.optim as optim


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


def test_answer_class_distribution(qa_pairs: list):
    """응/아니로 시작하는 답변의 실제 비율을 정확히 집계"""
    yes_count = sum(1 for _, a in qa_pairs if a.startswith("응"))
    no_count = sum(1 for _, a in qa_pairs if a.startswith("아니"))
    other_count = len(qa_pairs) - yes_count - no_count

    print(f"전체 QA 쌍: {len(qa_pairs)}개")
    print(f"'응'으로 시작: {yes_count}개")
    print(f"'아니'로 시작: {no_count}개")
    print(f"그 외: {other_count}개")
    print(f"응:아니 비율 = {yes_count}:{no_count} (약 {yes_count/no_count:.1f}:1)")

    assert other_count == 0, "응/아니 둘 다 아닌 답변이 존재함 (분류 기준 재확인 필요)"
    return yes_count, no_count


def greedy_generate_first_token(model, tokenizer, prompt: str) -> str:
    """
    확률적 샘플링(temperature, top_k) 없이, 다음 토큰 중 확률이 가장 높은 것만
    선택하는 greedy decoding으로 첫 토큰 하나만 생성해서 확인.
    """
    input_ids = tokenizer.encode(prompt)
    input_tensor = torch.tensor([input_ids])

    with torch.no_grad():
        logits = model(input_tensor)[:, -1, :]
        next_token_id = torch.argmax(logits, dim=-1).item()

    return tokenizer.decode([next_token_id])


def test_generation_accuracy_by_expected_class(model, tokenizer, prompts_with_expected: list):
    """
    각 프롬프트가 실제로 무엇을 기대하는지(expected: '응' 또는 '아니')와 함께 받아서,
    클래스별로 정확도를 따로 측정한다. 클래스 불균형이 실제 문제라면, '아니'가
    정답인 그룹에서 정확도가 뚜렷하게 낮게 나와야 한다(모델이 소수 클래스를
    무시하고 다수 클래스인 '응'으로 도피하는 경향).
    """
    results = {"응": [], "아니": []}
    for prompt, expected in prompts_with_expected:
        first_token = greedy_generate_first_token(model, tokenizer, prompt)
        is_correct = expected in first_token
        results[expected].append(is_correct)
        print(f"  프롬프트: {prompt!r:24s} 기대={expected!r} -> 생성 첫 토큰: {first_token!r} "
              f"({'정답' if is_correct else '오답'})")

    print()
    for expected_class, outcomes in results.items():
        if not outcomes:
            continue
        accuracy = sum(outcomes) / len(outcomes)
        print(f"'{expected_class}'가 정답인 그룹 정확도: {sum(outcomes)}/{len(outcomes)} "
              f"({accuracy*100:.1f}%)")
    return results


def main():
    print("=== B단계 진단: 클래스 불균형 확인 ===\n")

    qa_pairs = load_qa_pairs("src/custom_transformer/scripts/raw_data/korean_qa.txt")

    print("--- 1. 데이터 분포 집계 ---")
    yes_count, no_count = test_answer_class_distribution(qa_pairs)

    print("\n--- 2. 모델 학습 (train.py와 동일한 절차, 검증 목적상 축소) ---")
    flat_corpus = [q for q, _ in qa_pairs] + [a for _, a in qa_pairs]
    tokenizer = BPETokenizer(vocab_size=300)
    tokenizer.train(flat_corpus)
    vocab_size = len(tokenizer.token_to_id)

    model = TransformerLanguageModel(
        vocab_size=vocab_size, d_model=256, num_heads=8,
        num_layers=4, d_ff=1024, max_len=512, dropout=0.1
    )
    model.train()

    criterion = nn.CrossEntropyLoss(ignore_index=IGNORE_INDEX)
    optimizer = optim.Adam(model.parameters(), lr=3e-4)
    eos_id = tokenizer.token_to_id[tokenizer.eos_token]

    for epoch in range(50):
        for question, answer in qa_pairs:
            question_ids = tokenizer.encode(question)
            answer_ids = tokenizer.encode(answer) + [eos_id]
            if len(question_ids) == 0 or len(answer_ids) == 0:
                continue
            inputs, labels = build_qa_training_pair(question_ids, answer_ids)
            inputs_tensor = torch.tensor([inputs])
            labels_tensor = torch.tensor([labels])
            outputs = model(inputs_tensor)
            loss = criterion(outputs.view(-1, vocab_size), labels_tensor.view(-1))
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

    print("\n--- 3-0. 학습 데이터 원문 자체를 암기했는지 먼저 확인 ---")
    print("(변형 없이 학습에 실제로 있던 질문을 그대로 넣었을 때, 정확한 답이 나오는지)")
    memorization_check_prompts = [
        "내일 운동 할 거야?",   # 정답: 응, 운동 할 거야
        "내일 공부 할 거야?",   # 정답: 응, 공부 할 거야
        "내일 베이킹 할 거야?", # 정답: 응, 베이킹 할 거야
        "오늘 출근 할 거야?",   # 정답: 응, 출근 할 거야
        "오늘 친구 만날 거야?", # 정답: 응, 친구 만날 거야
    ]
    memorized_correctly = 0
    for prompt in memorization_check_prompts:
        first_token = greedy_generate_first_token(model, tokenizer, prompt)
        is_correct = "응" in first_token
        print(f"  프롬프트(원문): {prompt!r} -> 첫 토큰: {first_token!r} "
              f"({'정답(응)' if is_correct else '암기 실패'})")
        if is_correct:
            memorized_correctly += 1
    print(f"\n원문 그대로 넣었을 때 정답률: {memorized_correctly}/{len(memorization_check_prompts)} "
          f"({memorized_correctly/len(memorization_check_prompts)*100:.1f}%)")

    print("\n--- 3. 미학습 프롬프트에 대한 클래스별 생성 정확도 확인 ---")
    model.eval()

    # 원본 데이터에서 "번복"(동일 질문에 응/아니 둘 다 등장)이 없이,
    # 항상 '응'으로만 고정되어 있던 명사(운동, 공부, 베이킹, 출근, 친구)와,
    # 항상 '아니'로만 고정되어 있던 명사(조깅, 쇼핑, 여행) 둘 다 사용한다.
    # 헬스장/피크닉/회의/영화처럼 원본에서 이미 중복 질문으로 번복되던 명사는
    # 제외한다 -- 그 경우는 편향이 아니라 원래부터 정답이 하나로 정해지지
    # 않은 질문이므로, 순수한 클래스 불균형 진단에 섞이면 안 된다.
    prompts_with_expected = [
        ("내일 운동 갈 거야?", "응"),      # 원본 "내일 운동 할 거야?" -> 응
        ("오늘 공부 할 거야?", "응"),      # 원본 "내일 공부 할 거야?" -> 응
        ("오늘 베이킹 할 거야?", "응"),    # 원본 "내일 베이킹 할 거야?" -> 응
        ("내일 출근 할 거야?", "응"),      # 원본 "오늘 출근 할 거야?" -> 응
        ("내일 친구 만날 거야?", "응"),    # 원본 "오늘 친구 만날 거야?" -> 응
        # C단계 재진단의 핵심: 클래스 불균형(응 17개, 아니 7개)이 실제 문제라면,
        # 소수 클래스인 '아니' 그룹에서 정확도가 뚜렷하게 낮아야 한다.
        # 요일(오늘/내일)을 바꾸면 원본의 다른 행(응 케이스)과 겹치는 경우가 있어
        # (예: 여행), 요일·명사 조합은 원본의 '아니' 케이스 그대로 유지하고
        # 어미(할/갈/볼 등)만 바꿔서 진짜 미학습 문장을 만든다.
        ("내일 조깅 갈 거야?", "아니"),    # 원본 "내일 조깅 할 거야?"(할->갈) -> 아니
        ("오늘 쇼핑 할 거야?", "아니"),    # 원본 "오늘 쇼핑 갈 거야?"(갈->할) -> 아니
        ("내일 여행 떠날 거야?", "아니"),  # 원본 "내일 여행 갈 거야?"(갈->떠날) -> 아니
    ]
    results = test_generation_accuracy_by_expected_class(model, tokenizer, prompts_with_expected)

    yes_accuracy = sum(results["응"]) / len(results["응"]) if results["응"] else None
    no_accuracy = sum(results["아니"]) / len(results["아니"]) if results["아니"] else None
    print(f"\n결론: 데이터 응:아니 비율은 {yes_count}:{no_count}였고, "
          f"미학습 프롬프트에서 '응' 그룹 정확도는 {yes_accuracy*100:.1f}%, "
          f"'아니' 그룹 정확도는 {no_accuracy*100:.1f}%였습니다.")


if __name__ == "__main__":
    main()