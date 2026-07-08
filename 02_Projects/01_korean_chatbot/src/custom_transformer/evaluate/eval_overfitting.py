"""
D단계(과적합) 진단 스크립트.

목적:
    "학습 loss는 계속 줄어드는데 검증 loss는 어느 시점부터 늘어난다"는
    과적합의 전형적인 신호가 실제로 나타나는지 확인한다.

방법:
    33개 데이터 중 일부(7개)를 학습에서 완전히 제외한 검증 세트로 떼어두고,
    나머지 26개로만 학습하면서 매 epoch마다 "학습 loss"와 "검증 loss"를
    모두 측정해 그 추이를 비교한다.

판단 기준:
    - 학습 loss와 검증 loss가 함께 감소하다가 계속 낮게 유지되면 과적합 약함
    - 검증 loss가 어느 epoch부터 다시 증가하기 시작하면(학습 loss는 계속
      감소) 과적합의 명확한 신호
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


def compute_avg_loss(model, tokenizer, criterion, eos_id, vocab_size, pairs, update=False, optimizer=None):
    """
    pairs 전체에 대한 평균 loss를 계산한다.
    update=True면 학습(gradient 갱신)까지 수행, False면 순수 평가만 한다.
    """
    total_loss, count = 0.0, 0
    context = torch.enable_grad() if update else torch.no_grad()
    with context:
        for question, answer in pairs:
            question_ids = tokenizer.encode(question)
            answer_ids = tokenizer.encode(answer) + [eos_id]
            if len(question_ids) == 0 or len(answer_ids) == 0:
                continue
            inputs, labels = build_qa_training_pair(question_ids, answer_ids)
            inputs_tensor = torch.tensor([inputs])
            labels_tensor = torch.tensor([labels])
            outputs = model(inputs_tensor)
            loss = criterion(outputs.view(-1, vocab_size), labels_tensor.view(-1))
            if update:
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
            total_loss += loss.item()
            count += 1
    return total_loss / count


def main():
    print("=== D단계 진단: train/validation 분리를 통한 과적합 확인 ===\n")

    qa_pairs = load_qa_pairs("src/custom_transformer/scripts/raw_data/korean_qa.txt")
    print(f"전체 데이터: {len(qa_pairs)}개")

    # validation 7개: 응 4개, 아니 3개가 섞이도록 구성 (전체 뒤쪽에서 추출)
    # 각 명사가 train에도 최소 1개는 남도록, C단계에서 새로 추가한 명사들 위주로 validation 구성
    validation_questions = {
        "오늘 청소 할 거야?",       # 응 (train에 "요가", "캠핑" 등 다른 응 사례 남음)
        "내일 캠핑 갈 거야?",       # 응
        "오늘 요가 할 거야?",       # 응
        "내일 요가 갈 거야?",       # 응
        "오늘 낚시 갈 거야?",       # 아니
        "오늘 등산 갈 거야?",       # 아니
        "내일 수영 갈 거야?",       # 아니
    }
    train_pairs = [p for p in qa_pairs if p[0] not in validation_questions]
    val_pairs = [p for p in qa_pairs if p[0] in validation_questions]

    print(f"train: {len(train_pairs)}개, validation: {len(val_pairs)}개\n")

    flat_corpus = [q for q, _ in qa_pairs] + [a for _, a in qa_pairs]  # tokenizer는 전체로 학습(어휘 확보 목적)
    tokenizer = BPETokenizer(vocab_size=300)
    tokenizer.train(flat_corpus)
    vocab_size = len(tokenizer.token_to_id)

    model = TransformerLanguageModel(
        vocab_size=vocab_size, d_model=256, num_heads=8,
        num_layers=4, d_ff=1024, max_len=512, dropout=0.1
    )

    criterion = nn.CrossEntropyLoss(ignore_index=IGNORE_INDEX)
    optimizer = optim.Adam(model.parameters(), lr=3e-4)
    eos_id = tokenizer.token_to_id[tokenizer.eos_token]

    num_epochs = 100
    print(f"{'epoch':>6} | {'train_loss':>12} | {'val_loss':>12}")
    history = []
    for epoch in range(1, num_epochs + 1):
        model.train()
        train_loss = compute_avg_loss(model, tokenizer, criterion, eos_id, vocab_size,
                                       train_pairs, update=True, optimizer=optimizer)
        model.eval()
        val_loss = compute_avg_loss(model, tokenizer, criterion, eos_id, vocab_size,
                                     val_pairs, update=False)
        history.append((epoch, train_loss, val_loss))
        if epoch % 10 == 0 or epoch == 1:
            print(f"{epoch:>6} | {train_loss:>12.4f} | {val_loss:>12.4f}")

    print("\n=== 과적합 신호 확인 ===")
    min_val_loss_epoch = min(history, key=lambda h: h[2])
    final_epoch = history[-1]
    print(f"validation loss가 최소였던 epoch: {min_val_loss_epoch[0]} (val_loss={min_val_loss_epoch[2]:.4f})")
    print(f"마지막 epoch({final_epoch[0]}): train_loss={final_epoch[1]:.4f}, val_loss={final_epoch[2]:.4f}")

    if final_epoch[2] > min_val_loss_epoch[2] * 1.1:
        print("\n[결론] validation loss가 최솟값 대비 10% 이상 다시 증가했습니다.")
        print("학습 loss는 계속 낮은데 검증 loss만 다시 오르는 전형적인 과적합 신호입니다.")
    else:
        print("\n[결론] validation loss가 크게 재상승하지 않았습니다. 뚜렷한 과적합 신호는")
        print("관찰되지 않았으나, validation 표본(7개)이 적어 결론의 신뢰도에 한계가 있습니다.")


if __name__ == "__main__":
    main()