<div align="center">

# Who Writes What: Unveiling the Impact of Author Roles on AI-generated Text Detection [ACL 2025]

<p align="center">
  <a href="https://aclanthology.org/2025.acl-long.1292.pdf">
    <img src="https://img.shields.io/badge/Paper-ACL%202025-blue?style=for-the-badge&logo=adobeacrobatreader" alt="Paper">
  </a>
  <a href="https://huggingface.co/datasets/leejamesssss/AuthorAwareDetectionBench">
    <img src="https://img.shields.io/badge/Dataset-%F0%9F%A4%97%20Hugging%20Face-yellow?style=for-the-badge" alt="HuggingFace Dataset">
  </a>
  <a href="https://github.com/leejamesss/AuthorAwareDetection">
    <img src="https://img.shields.io/badge/GitHub-Repo-black?style=for-the-badge&logo=github" alt="GitHub">
  </a>
</p>

<img src="assets/teaser.jpg" alt="Teaser Image" style="width: 100%; height: auto; border-radius: 10px;" />

</div>


## Overview
**AuthorAwareDetection** is the official repository for the ACL 2025 paper *"[Who Writes What: Unveiling the Impact of Author Roles on AI-generated Text Detection](https://aclanthology.org/2025.acl-long.1292.pdf)"*.

The current AI text detection field largely overlooks the influence of author characteristics. **AuthorAwareDetectionBench** is a benchmark designed to investigate how sociolinguistic attributes, including Gender, CEFR Proficiency, Academic Field, and Language Environment, impact the performance of AI text detectors.

We employ 12 diverse LLMs to generate parallel texts that mirror the demographic profiles of human authors from the ICNALE corpus, creating a controlled environment for bias analysis.


## Data Access
We host the AI-generated portion of our benchmark on Hugging Face. To load our data, run:

```python
from datasets import load_dataset

dataset = load_dataset("leejamesssss/AuthorAwareDetectionBench", split="train")
```

Note on Human Data: For the human-authored portion, please download the [ICNALE Corpus](http://language.sakura.ne.jp/icnale/) separately. You can then use the scripts provided in this repository to merge the human texts with our AI dataset.


## License

This dataset is licensed under **CC BY-NC 4.0** (AI text & metadata) and **MIT** (Code).

> **Note:** Consistent with the [ICNALE Terms of Use](http://language.sakura.ne.jp/icnale/), this repository does not distribute original human-authored texts. Researchers must obtain the ICNALE corpus separately to reproduce the full benchmark.



## Citation

If you use this dataset in your research, please cite our paper:

```bibtex
@misc{li2025writeswhatunveilingimpact,
      title={Who Writes What: Unveiling the Impact of Author Roles on AI-generated Text Detection},
      author={Jiatao Li and Xiaojun Wan},
      year={2025},
      eprint={2502.12611},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2502.12611},
}
```

Please also credit the original ICNALE corpus:

```
@article{ishikawa2013icnale,
  author = {Ishikawa, Shin'ichiro},
  title = {The ICNALE and sophisticated contrastive interlanguage analysis of Asian learners of English},
  journal = {Learner corpus studies in Asia and the world},
  volume = {1},
  year = {2013},
  pages = {91-118}
}
```





