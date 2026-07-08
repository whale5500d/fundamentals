"""
A단계(weight tying 버그) 재검증 스크립트.

목적:
    transformer_decoder.py를 deepcopy로 수정한 뒤, 실제로 학습을 거치면서
    4개 층의 가중치가 서로 다른 값으로 발산하는지 확인한다.

    파라미터 개수/이름만으로는 "독립된 객체인가"만 확인할 수 있다.
    "실제로 다르게 학습되는가"는 학습을 거쳐야만 확인 가능하다 -- 예를 들어
    deepcopy는 정확히 적용됐지만, 4개 층이 우연히 똑같은 gradient를 받아서
    학습 후에도 여전히 같은 값을 유지하는 경우도 이론적으로 가능하기 때문이다.

검증 절차:
    1. 학습 전, 4개 층의 self_attention.q_linear.weight를 각각 저장해둔다.
       (이 시점에는 4개 층이 서로 값이 같을 수도, 다를 수도 있다 -- 초기화
        방식에 따라 다르므로 이 자체는 중요하지 않다. 중요한 건 "학습 후"다.)
    2. 몇 epoch 학습을 진행한다.
    3. 학습 후, 4개 층 사이의 쌍(pairwise) L2 거리를 계산한다.
       거리가 0에 가까우면 "여전히 같은 값을 유지하고 있다"는 뜻이고,
       거리가 뚜렷하게 0보다 크면 "서로 다르게 학습됐다"는 증거다.
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


def get_layer_weight_snapshot(model: TransformerLanguageModel) -> list:
    """4개 층 각각의 q_linear.weight를 복사해서 리스트로 반환 (학습 중 변경과 무관하게 스냅샷)"""
    return [
        layer.self_attention.q_linear.weight.detach().clone()
        for layer in model.decoder.layers
    ]


def pairwise_l2_distances(weights: list) -> list:
    """리스트 안의 모든 (i, j) 쌍에 대해 L2 거리를 계산"""
    distances = []
    num_layers = len(weights)
    for i in range(num_layers):
        for j in range(i + 1, num_layers):
            dist = torch.norm(weights[i] - weights[j]).item()
            distances.append((i, j, dist))
    return distances


def test_layers_are_independent_objects(model: TransformerLanguageModel):
    """deepcopy가 적용되어 4개 층이 서로 다른 파이썬 객체인지 확인 (파라미터 값과 무관하게)"""
    layer_ids = [id(layer) for layer in model.decoder.layers]
    assert len(set(layer_ids)) == len(layer_ids), (
        f"4개 층 중 일부가 같은 객체를 공유하고 있음: {layer_ids}"
    )
    print(f"PASS: test_layers_are_independent_objects (4개 층의 객체 id 전부 다름: {layer_ids})")


def test_layers_diverge_after_training(model: TransformerLanguageModel,
                                        weights_before: list, weights_after: list,
                                        min_distance: float = 1e-4):
    """
    핵심 검증: 학습 전에는 초기화 방식에 따라 층별 가중치가 우연히 비슷할 수 있지만,
    학습 후에는 서로 다른 gradient를 받아 뚜렷하게 달라져야 한다.
    """
    distances_before = pairwise_l2_distances(weights_before)
    distances_after = pairwise_l2_distances(weights_after)

    print("학습 전 층 간 L2 거리:")
    for i, j, dist in distances_before:
        print(f"  layer{i} vs layer{j}: {dist:.6f}")

    print("학습 후 층 간 L2 거리:")
    for i, j, dist in distances_after:
        print(f"  layer{i} vs layer{j}: {dist:.6f}")

    all_diverged = all(dist > min_distance for _, _, dist in distances_after)
    assert all_diverged, (
        f"학습 후에도 일부 층의 가중치가 거의 동일함 (여전히 tying 문제 의심): {distances_after}"
    )
    print(f"PASS: test_layers_diverge_after_training "
          f"(학습 후 모든 층 쌍의 L2 거리가 {min_distance} 초과, 독립적으로 학습됨 확인)")


def main():
    print("=== A단계 재검증: weight tying 수정 후 학습 발산 확인 ===\n")

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

    # 1단계: 독립된 객체인지 먼저 확인 (파라미터 값과 무관한 구조적 검증)
    test_layers_are_independent_objects(model)

    # 2단계: 학습 전 스냅샷
    weights_before = get_layer_weight_snapshot(model)

    # 3단계: 짧게 학습 진행 (검증 목적이므로 몇 epoch만)
    criterion = nn.CrossEntropyLoss(ignore_index=IGNORE_INDEX)
    optimizer = optim.Adam(model.parameters(), lr=3e-4)
    eos_id = tokenizer.token_to_id[tokenizer.eos_token]

    for epoch in range(20):
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

    # 4단계: 학습 후 스냅샷 및 발산 여부 확인
    weights_after = get_layer_weight_snapshot(model)
    test_layers_diverge_after_training(model, weights_before, weights_after)

    print("\n모든 검증 통과: A단계(weight tying 버그) 수정이 완전히 확인됨.")


if __name__ == "__main__":
    main()