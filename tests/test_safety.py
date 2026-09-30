"""安全护栏回归测试。

运行方式：
    python tests/test_safety.py

覆盖两类场景：
1. 不应误报 —— 咨询类提问（「如何预防中风」）、否定陈述（「我没有胸痛」）、
   分诊页常见症状（「胸闷」）都不应触发急救提示。
2. 不应漏报 —— 真实危急表述必须触发。
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import safety  # noqa: E402

# (输入文本, 期望是否触发紧急)
EMERGENCY_CASES: list[tuple[str, bool]] = [
    # ---- 不应触发 ----
    ("如何预防中风？", False),
    ("怎么预防心肌梗死", False),
    ("中风是什么原因引起的", False),
    ("我没有胸痛，就是有点累", False),
    ("胸闷", False),
    ("胸闷是什么原因", False),
    ("胸闷应该怎么缓解", False),
    ("听说一氧化碳中毒很危险，怎么预防", False),
    ("介绍一下中风的前兆有哪些", False),
    ("心悸有哪些症状", False),
    ("孩子高热惊厥怎么预防", False),
    # ---- 应该触发 ----
    ("我胸口突然剧烈疼痛，压榨感，伴大汗", True),
    ("突然心跳骤停怎么办", True),
    ("他意识丧失了，叫不醒", True),
    ("一直大出血止不住", True),
    ("老人突然一侧肢体无力，说话不清", True),
    ("胸闷，持续不缓解，冒冷汗", True),
    ("剧烈头痛，从没这么痛过", True),
    ("误食了农药", True),
    ("患者呼吸停止了", True),
]

# 心理危机检测：(文本, 期望是否触发)
CRISIS_CASES: list[tuple[str, bool]] = [
    ("我不想活了", True),
    ("我想自杀", True),
    ("最近很焦虑，怎么缓解", False),
]


def _run(title: str, cases: list[tuple[str, bool]], detector) -> int:
    print("=" * 62)
    print(title)
    print("=" * 62)
    failed = 0
    for text, expect in cases:
        hit = detector(text)
        ok = (hit is not None) == expect
        failed += 0 if ok else 1
        detail = f"命中「{hit}」" if hit else "未触发"
        print(
            f"[{'PASS' if ok else 'FAIL'}] {text[:32]:<34} "
            f"期望={'触发' if expect else '不触发':<6} 实际={detail}"
        )
    print()
    return failed


def main() -> int:
    failed = _run("紧急症状检测", EMERGENCY_CASES, safety.detect_emergency)
    failed += _run("心理危机检测", CRISIS_CASES, safety.detect_crisis)

    total = len(EMERGENCY_CASES) + len(CRISIS_CASES)
    print("-" * 62)
    print(f"通过 {total - failed} / {total}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
