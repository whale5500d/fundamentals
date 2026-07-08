"""
C단계(클래스 불균형) 반복 검증.

목적:
    33개로 확장된 데이터에서 "아니" 그룹 정확도가 100%로 나온 게
    데이터 확장의 실제 효과인지, 우연한 학습 결과인지 확인한다.

방법:
    torch.manual_seed()를 고정하지 않은 채로, "학습 -> 평가" 파이프라인을
    5회 반복 실행한다. 매번 모델이 무작위로 새로 초기화되고 처음부터
    다시 학습되므로, 5번의 독립적인 시행(trial)이 된다.

판단 기준:
    - 5회 전부(혹은 대부분) "아니" 그룹 정확도가 높게(예: 80% 이상) 나오면
      -> 데이터 확장의 안정적인 효과로 판단
    - 5회 중 일부만 높고 나머지는 낮게 들쭉날쭉하면
      -> 지난번 100%는 우연이었을 가능성이 크다는 뜻
"""

import torch
import torch.nn as nn
import torch.optim as optim
from custom_transformer.transformer_model import TransformerLanguageModel
from custom_transformer.tokenizer.bpe_tokenizer import BPETokenizer
from custom_transformer.scripts.utils.qa_collate import build_qa_training_pair, IGNORE_INDEX


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


def greedy_generate_first_token(model, tokenizer, prompt: str) -> str:
    input_ids = tokenizer.encode(prompt)
    input_tensor = torch.tensor([input_ids])
    with torch.no_grad():
        logits = model(input_tensor)[:, -1, :]
        next_token_id = torch.argmax(logits, dim=-1).item()
    return tokenizer.decode([next_token_id])


def train_and_evaluate_once(qa_pairs, prompts_with_expected) -> dict:
    """학습 파이프라인 1회 실행 후, 클래스별 정확도를 반환 (seed 고정 없음)"""
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

    model.eval()
    results = {"응": [], "아니": []}
    for prompt, expected in prompts_with_expected:
        first_token = greedy_generate_first_token(model, tokenizer, prompt)
        is_correct = expected in first_token
        results[expected].append(is_correct)

    return {
        "응_정확도": sum(results["응"]) / len(results["응"]),
        "아니_정확도": sum(results["아니"]) / len(results["아니"]),
    }


def main():
    print("=== C단계 반복 검증: 데이터 확장(33개) 효과가 안정적인지 확인 ===\n")

    qa_pairs = load_qa_pairs("src/custom_transformer/scripts/raw_data/korean_qa.txt")
    print(f"학습 데이터 수: {len(qa_pairs)}개\n")

    prompts_with_expected = [
        ("내일 운동 갈 거야?", "응"),
        ("오늘 공부 할 거야?", "응"),
        ("오늘 베이킹 할 거야?", "응"),
        ("내일 출근 할 거야?", "응"),
        ("내일 친구 만날 거야?", "응"),
        ("내일 조깅 갈 거야?", "아니"),
        ("오늘 쇼핑 할 거야?", "아니"),
        ("내일 여행 떠날 거야?", "아니"),
    ]

    num_trials = 5
    all_results = []
    for trial in range(1, num_trials + 1):
        print(f"--- 시행 {trial}/{num_trials} (seed 고정 없음, 매번 새로 무작위 초기화) ---")
        result = train_and_evaluate_once(qa_pairs, prompts_with_expected)
        all_results.append(result)
        print(f"  '응' 그룹 정확도: {result['응_정확도']*100:.1f}%")
        print(f"  '아니' 그룹 정확도: {result['아니_정확도']*100:.1f}%\n")

    print("=== 5회 시행 요약 ===")
    yes_accuracies = [r["응_정확도"] for r in all_results]
    no_accuracies = [r["아니_정확도"] for r in all_results]

    print(f"'응' 그룹 정확도: {[f'{a*100:.0f}%' for a in yes_accuracies]}")
    print(f"  평균: {sum(yes_accuracies)/len(yes_accuracies)*100:.1f}%, "
          f"최솟값: {min(yes_accuracies)*100:.1f}%, 최댓값: {max(yes_accuracies)*100:.1f}%")
    print(f"'아니' 그룹 정확도: {[f'{a*100:.0f}%' for a in no_accuracies]}")
    print(f"  평균: {sum(no_accuracies)/len(no_accuracies)*100:.1f}%, "
          f"최솟값: {min(no_accuracies)*100:.1f}%, 최댓값: {max(no_accuracies)*100:.1f}%")

    stable = min(no_accuracies) >= 0.8
    print(f"\n판정: '아니' 그룹 정확도가 5회 모두 80% 이상인가: {stable}")
    if stable:
        print("-> 데이터 확장이 안정적인 효과를 낸 것으로 판단됩니다.")
    else:
        print("-> 결과가 들쭉날쭉하여, 이전 100%는 우연이었을 가능성이 있습니다.")


if __name__ == "__main__":
    main()