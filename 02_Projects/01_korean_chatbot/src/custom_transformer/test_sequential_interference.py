"""
가설 검증: batch_size=1, 셔플 없는 순차 학습이 "먼저 학습된 샘플을 나중에
학습된 샘플이 다시 흔드는" 간섭(interference)을 일으키는지 확인.

방법:
    학습이 전부 끝난 뒤(gradient 갱신 없이), 24개 QA 쌍 전체를 다시 한 번
    forward만 돌려서 각각의 loss를 개별적으로 측정한다.
    - 학습 중 출력된 epoch loss는 "그 샘플을 갱신하기 직전" 시점의 값이므로
      이번 재평가와 다를 수 있다.
    - 만약 재평가에서 특정 샘플(특히 파일 앞쪽에 있는 샘플)의 loss가
      학습 중 관찰된 값보다 눈에 띄게 높다면, 뒤에 처리된 샘플들의 학습이
      앞선 샘플의 적합을 흔들었다는 증거가 된다.
"""

import torch
import torch.nn as nn
from custom_transformer.transformer_model import TransformerLanguageModel
from custom_transformer.tokenizer.bpe_tokenizer import BPETokenizer
from custom_transformer.scripts.utils.qa_collate import build_qa_training_pair, IGNORE_INDEX
import torch.optim as optim

torch.manual_seed(42)  # 모델 초기화를 고정해서, 재실행/다른 스크립트와 결과를 비교 가능하게 함


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
    print("=== 순차 학습 간섭(interference) 가설 검증 ===\n")

    qa_pairs = load_qa_pairs("src/custom_transformer/scripts/raw_data/korean_qa.txt")
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

    # 원본 train.py와 동일하게 50 epoch, 셔플 없이 순차 학습
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

    # 학습 완전히 종료 후, gradient 갱신 없이 24개 전체를 다시 개별 평가
    print("--- 학습 종료 후, 24개 샘플 개별 재평가 (gradient 갱신 없음) ---\n")
    model.eval()
    per_sample_losses = []
    with torch.no_grad():
        for idx, (question, answer) in enumerate(qa_pairs):
            question_ids = tokenizer.encode(question)
            answer_ids = tokenizer.encode(answer) + [eos_id]
            if len(question_ids) == 0 or len(answer_ids) == 0:
                continue
            inputs, labels = build_qa_training_pair(question_ids, answer_ids)
            inputs_tensor = torch.tensor([inputs])
            labels_tensor = torch.tensor([labels])
            outputs = model(inputs_tensor)
            loss = criterion(outputs.view(-1, vocab_size), labels_tensor.view(-1))
            per_sample_losses.append(loss.item())
            print(f"  [{idx:2d}] {question!r:30s} -> loss={loss.item():.4f}")

    avg = sum(per_sample_losses) / len(per_sample_losses)
    max_loss_idx = per_sample_losses.index(max(per_sample_losses))
    print(f"\n재평가 평균 loss: {avg:.4f}")
    print(f"가장 loss가 높은 샘플: [{max_loss_idx}] {qa_pairs[max_loss_idx][0]!r} "
          f"(loss={per_sample_losses[max_loss_idx]:.4f})")

    high_loss_samples = [(i, l) for i, l in enumerate(per_sample_losses) if l > 1.0]
    print(f"\nloss가 1.0을 넘는(사실상 학습이 안 된) 샘플 개수: {len(high_loss_samples)}개")
    for i, l in high_loss_samples:
        print(f"  [{i}] {qa_pairs[i][0]!r} (loss={l:.4f})")

    # 핵심 추가 검증: 정답 시퀀스 전체 평균이 아니라, "응/아니가 갈리는 첫 토큰 하나"의
    # loss만 따로 떼어서 확인. 답변 뒤쪽(", 산책 할 거야" 등)은 어느 질문이든 패턴이
    # 비슷해서 쉽게 맞히므로, 전체 평균에 첫 토큰의 어려움이 희석될 수 있다.
    print("\n--- 첫 토큰(응/아니 분기점)만 개별 확인 + 같은 모델로 실제 greedy 생성 ---\n")
    with torch.no_grad():
        for idx, (question, answer) in enumerate(qa_pairs):
            question_ids = tokenizer.encode(question)
            answer_ids = tokenizer.encode(answer) + [eos_id]
            if len(question_ids) == 0 or len(answer_ids) == 0:
                continue

            # 첫 토큰만의 loss: 질문 마지막 토큰 위치에서, 정답(answer_ids[0])에 대한 개별 loss
            inputs, labels = build_qa_training_pair(question_ids, answer_ids)
            inputs_tensor = torch.tensor([inputs])
            outputs = model(inputs_tensor)
            first_answer_position = len(question_ids) - 1  # qa_collate.py의 mask_boundary와 동일
            first_token_logits = outputs[0, first_answer_position, :]
            first_token_target = torch.tensor(answer_ids[0])
            first_token_loss = nn.functional.cross_entropy(
                first_token_logits.unsqueeze(0), first_token_target.unsqueeze(0)
            ).item()

            # 같은 모델로 실제 greedy 생성 (질문만 입력, 첫 토큰 하나 예측)
            question_only_tensor = torch.tensor([question_ids])
            greedy_logits = model(question_only_tensor)[:, -1, :]
            greedy_token_id = torch.argmax(greedy_logits, dim=-1).item()
            greedy_token_text = tokenizer.decode([greedy_token_id])
            expected_token_text = tokenizer.decode([answer_ids[0]])

            match = "일치" if greedy_token_id == answer_ids[0] else "불일치"
            print(f"  [{idx:2d}] {question!r:22s} 정답 첫 토큰={expected_token_text!r:8s} "
                  f"첫토큰loss={first_token_loss:.4f}  greedy 생성={greedy_token_text!r:8s} ({match})")


if __name__ == "__main__":
    main()