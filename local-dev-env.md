# Environment

### Create conda env
```shell
conda create -y --name=gtbot python=3.9
```

### Remove conda env
```shell
conda env remove -y --name gtbot
```

### add jupyter kernel
```shell
conda activate gtbot
pip install ipykernel
python -m ipykernel install --user --name gtbot --display-name "GTBot"
```

### remove jupyter kernel
```shell
jupyter kernelspec uninstall -y gtbot
```
