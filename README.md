# README

**shLLeM**

**Version:** 0.0.1

**Copyright 2024 P.L. Harvey**

## Description

This package provides a *lightweight* solution to self-host
a text-generation, or other similar language model.
Currently, it is designed to work with openly available
models through HuggingFace (via the ```transformers``` library).

Future versions may extend these capabilities, dependent on the
requirements requested by the user(s) and the hardware available.

## Installation

1. Using ```pip```:

```{bash}
pip install shLLeM
```

2: Using ```git```:

```{bash}
git clone https://github.com/P-Harvey/shLLeM.git
```

3: Using ```Docker```:

```{bash}
docker build -t shLLeM .
docker run -d -p 8000:8000 shLLeM
```

## Package Structure

```{bash}
./shLLeM@0.0.1
    ├── LICENSE                 <Apache2.0 License>
    ├── NOTICE                  <License Notice>
    ├── README                  <You Are Here>
    ├── serve.py                <launch server>
    ├── setup                   <build scripts>
    │   ├── build.sh            <build a container>
    │   ├── distribute          <docker build script>
    │   ├── requirements.txt    <dependencies>
    │   └── setup.sh            <setup script>
    ├── shLLeM.py               <primary script>
```

## Remarks

shLLeM is still in its early stages of development. Be sure to
test any new features or updates thoroughly before using them
in production.

If you have any suggestions, ideas, or feedback, please don't
hesitate to reach out!

## Citations

```
@article{hui2024qwen2,
      title={Qwen2. 5-Coder Technical Report},
      author={Hui, Binyuan and Yang, Jian and Cui, Zeyu and Yang, Jiaxi and Liu, Dayiheng and Zhang, Lei and Liu, Tianyu and Zhang, Jiajun and Yu, Bowen and Dang, Kai and others},
      journal={arXiv preprint arXiv:2409.12186},
      year={2024}
}
@article{qwen2,
      title={Qwen2 Technical Report}, 
      author={An Yang and Baosong Yang and Binyuan Hui and Bo Zheng and Bowen Yu and Chang Zhou and Chengpeng Li and Chengyuan Li and Dayiheng Liu and Fei Huang and Guanting Dong and Haoran Wei and Huan Lin and Jialong Tang and Jialin Wang and Jian Yang and Jianhong Tu and Jianwei Zhang and Jianxin Ma and Jin Xu and Jingren Zhou and Jinze Bai and Jinzheng He and Junyang Lin and Kai Dang and Keming Lu and Keqin Chen and Kexin Yang and Mei Li and Mingfeng Xue and Na Ni and Pei Zhang and Peng Wang and Ru Peng and Rui Men and Ruize Gao and Runji Lin and Shijie Wang and Shuai Bai and Sinan Tan and Tianhang Zhu and Tianhao Li and Tianyu Liu and Wenbin Ge and Xiaodong Deng and Xiaohuan Zhou and Xingzhang Ren and Xinyu Zhang and Xipin Wei and Xuancheng Ren and Yang Fan and Yang Yao and Yichang Zhang and Yu Wan and Yunfei Chu and Yuqiong Liu and Zeyu Cui and Zhenru Zhang and Zhihao Fan},
      journal={arXiv preprint arXiv:2407.10671},
      year={2024}
}
```
