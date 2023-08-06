# huggingface_tool

Tools for loading, upload, managing huggingface models and datasets


## Installation

`pip install huggingface_tool`

## Usage

- Download and save tokenizer with: `htool save-tk <tokenizer_name> <save_dir>`
  - For example: `htool save-tk gpt2 ./gpt2 `
- Download and save dataset with: `htool save-data <dataset_name> <save_dir>`
  - For example: `htool save-data daily_dialog ./daily_dialog`
- Download and save diffusion models with: `htool save-dm <model_name> <save_dir>`
  - For example: `htool save-dm google/ddpm-cat-256 ./google/`


## Citing huggingface_tool

If our work has been helpful to you, please feel free to cite us:
```latex
@misc{huggingface_tool2023,
    title={huggingface_tool},
    author={OpenRL Contributors},
    publisher = {GitHub},
    howpublished = {\url{https://github.com/OpenRL-Lab/huggingface_tool}},
    year={2023},
}
```