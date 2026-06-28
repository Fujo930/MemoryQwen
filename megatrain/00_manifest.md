# MegaTrain Manifest

## Checkpoints

| checkpoint | status | tokens | knowledge | eval |
|------------|:------:|:------:|:---------:|:----:|
| M1 | COMPLETE | — | — | — |
| M2 | COMPLETE | 5.12M | 22,211 | 200 questions |
| **M3** | **COMPLETE** | **11.27M** | **43,645** | **312 questions** |

## M3 Details
- Full eval: 300 questions executed
- Real critical violations: 0
- Judge false positives: 36 (documented)
- Latency: 3.6s avg (30-question smoke)
- GPU: RTX 4080 Laptop, 94% util during inference

## Next
- v0.1.5: Internet Query
- M4: TBD after Retrieval Quality v2
