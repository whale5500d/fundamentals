"""
D단계(과적합) 개선 비교.

지난 진단(test_overfitting.py)과 동일한 train/validation 분리, 동일한
측정 방식을 유지한 채, 아래 3가지 조건을 순서대로 적용해서 효과를 비교한다.

    베이스라인: 기존 설정 그대로 (d_model=256, num_layers=4, dropout=0.1, 100 epoch)
    개선 1: 조기 종료 (validation loss가 10 epoch 연속 개선 안 되면 중단)
    개선 2: 모델 축소 (d_model=64, num_layers=2, d_ff=256) + 조기 종료
    개선 3: dropout 상향 (dropout=0.4) + 조기 종료 (모델 크기는 원본 유지)

비교 기준: 각 조건의 "validation loss 최솟값"과 "그 지점 이후 반등 폭"
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


def run_experiment(name: str, train_pairs, val_pairs, tokenizer, vocab_size, eos_id,
                    d_model: int, num_layers: int, d_ff: int, dropout: float,
                    max_epochs: int, use_early_stopping: bool, patience: int = 10):
    """조건 하나를 학습시키고, 결과(최선 validation loss, 반등 여부, 실제 학습 epoch 수)를 반환"""
    print(f"\n{'='*60}")
    print(f"[{name}] d_model={d_model}, num_layers={num_layers}, d_ff={d_ff}, "
          f"dropout={dropout}, early_stopping={use_early_stopping}")
    print('='*60)

    model = TransformerLanguageModel(
        vocab_size=vocab_size, d_model=d_model, num_heads=max(1, d_model // 32),
        num_layers=num_layers, d_ff=d_ff, max_len=512, dropout=dropout
    )
    criterion = nn.CrossEntropyLoss(ignore_index=IGNORE_INDEX)
    optimizer = optim.Adam(model.parameters(), lr=3e-4)

    best_val_loss = float('inf')
    epochs_without_improvement = 0
    history = []
    stopped_epoch = max_epochs

    for epoch in range(1, max_epochs + 1):
        model.train()
        train_loss = compute_avg_loss(model, tokenizer, criterion, eos_id, vocab_size,
                                       train_pairs, update=True, optimizer=optimizer)
        model.eval()
        val_loss = compute_avg_loss(model, tokenizer, criterion, eos_id, vocab_size,
                                     val_pairs, update=False)
        history.append((epoch, train_loss, val_loss))

        if val_loss < best_val_loss:
            best_val_loss = val_loss
            epochs_without_improvement = 0
        else:
            epochs_without_improvement += 1

        if epoch % 10 == 0 or epoch == 1:
            print(f"  epoch {epoch:>4} | train_loss={train_loss:.4f} | val_loss={val_loss:.4f}")

        if use_early_stopping and epochs_without_improvement >= patience:
            print(f"  -> {patience} epoch 연속 개선 없어 조기 종료 (epoch {epoch})")
            stopped_epoch = epoch
            break

    final_val_loss = history[-1][2]
    rebound_pct = (final_val_loss - best_val_loss) / best_val_loss * 100

    print(f"  최종 결과: best_val_loss={best_val_loss:.4f} (실제 종료 epoch={stopped_epoch}), "
          f"마지막 val_loss={final_val_loss:.4f}, 반등폭={rebound_pct:+.1f}%")

    return {
        "name": name, "best_val_loss": best_val_loss, "final_val_loss": final_val_loss,
        "rebound_pct": rebound_pct, "stopped_epoch": stopped_epoch,
    }


def main():
    print("=== D단계 개선 비교: 베이스라인 vs 조기종료 vs 모델축소 vs dropout상향 ===")

    qa_pairs = load_qa_pairs("src/custom_transformer/scripts/raw_data/korean_qa.txt")
    validation_questions = {
        "오늘 청소 할 거야?", "내일 캠핑 갈 거야?", "오늘 요가 할 거야?", "내일 요가 갈 거야?",
        "오늘 낚시 갈 거야?", "오늘 등산 갈 거야?", "내일 수영 갈 거야?",
    }
    train_pairs = [p for p in qa_pairs if p[0] not in validation_questions]
    val_pairs = [p for p in qa_pairs if p[0] in validation_questions]
    print(f"train: {len(train_pairs)}개, validation: {len(val_pairs)}개")

    flat_corpus = [q for q, _ in qa_pairs] + [a for _, a in qa_pairs]
    tokenizer = BPETokenizer(vocab_size=300)
    tokenizer.train(flat_corpus)
    vocab_size = len(tokenizer.token_to_id)
    eos_id = tokenizer.token_to_id[tokenizer.eos_token]

    results = []

    # 베이스라인: 기존 설정 그대로, 100 epoch 고정 (조기 종료 없음) -- 지난 진단과 동일 조건
    results.append(run_experiment(
        "베이스라인", train_pairs, val_pairs, tokenizer, vocab_size, eos_id,
        d_model=256, num_layers=4, d_ff=1024, dropout=0.1,
        max_epochs=100, use_early_stopping=False
    ))

    # 개선 1: 조기 종료만 추가 (모델 크기, dropout은 베이스라인과 동일)
    results.append(run_experiment(
        "개선1_조기종료", train_pairs, val_pairs, tokenizer, vocab_size, eos_id,
        d_model=256, num_layers=4, d_ff=1024, dropout=0.1,
        max_epochs=100, use_early_stopping=True, patience=10
    ))

    # 개선 2: 모델 축소 + 조기 종료
    results.append(run_experiment(
        "개선2_모델축소", train_pairs, val_pairs, tokenizer, vocab_size, eos_id,
        d_model=64, num_layers=2, d_ff=256, dropout=0.1,
        max_epochs=100, use_early_stopping=True, patience=10
    ))

    # 개선 3: dropout 상향 + 조기 종료 (모델 크기는 베이스라인과 동일)
    results.append(run_experiment(
        "개선3_dropout상향", train_pairs, val_pairs, tokenizer, vocab_size, eos_id,
        d_model=256, num_layers=4, d_ff=1024, dropout=0.4,
        max_epochs=100, use_early_stopping=True, patience=10
    ))

    # 조합 실험: 개선2(모델 축소)를 기반으로, dropout을 경미하게(0.15, 0.2) 얹어봄
    results.append(run_experiment(
        "조합1_축소+dropout0.15", train_pairs, val_pairs, tokenizer, vocab_size, eos_id,
        d_model=64, num_layers=2, d_ff=256, dropout=0.15,
        max_epochs=100, use_early_stopping=True, patience=10
    ))
    results.append(run_experiment(
        "조합2_축소+dropout0.2", train_pairs, val_pairs, tokenizer, vocab_size, eos_id,
        d_model=64, num_layers=2, d_ff=256, dropout=0.2,
        max_epochs=100, use_early_stopping=True, patience=10
    ))

    # 조합 실험: 개선2(모델 축소) 기반으로, patience를 더 타이트하게(5) 줄여봄
    results.append(run_experiment(
        "조합3_축소+patience5", train_pairs, val_pairs, tokenizer, vocab_size, eos_id,
        d_model=64, num_layers=2, d_ff=256, dropout=0.1,
        max_epochs=100, use_early_stopping=True, patience=5
    ))

    print(f"\n\n{'='*70}")
    print("=== 전체 비교 요약 ===")
    print(f"{'조건':<20} {'best_val_loss':>15} {'종료epoch':>10} {'반등폭':>10}")
    for r in results:
        print(f"{r['name']:<20} {r['best_val_loss']:>15.4f} {r['stopped_epoch']:>10} "
              f"{r['rebound_pct']:>9.1f}%")


if __name__ == "__main__":
    main()