# QFSL-benchmark

This repository provides an experimental framework for evaluating the performance and accuracy trade-offs of model quantization in Split Federated Learning systems. This code was developed as part of my master's thesis entitled "Análise de desempenho da quantização em soluções de aprendizado dividido federado" (Performance Analysis of Quantization in Federated Split Learning Solutions).

The experiments are divided into two stages: training and inference. During training, models can be trained locally while simulating a Federated Split Learning (FSL) setup. During inference, the system can be executed in a distributed environment, with components communicating via gRPC.

The training phase allows evaluating the model accuracy before and after client-side quantization. Computational metrics (e.g., execution time and memory usage) are not considered during training, since quantization is applied only for the inference stage.

The inference phase is executed in a distributed environment using gRPC for evaluation of the computational benefits of quantization. During this stage, metrics such as execution time, peak memory usage, model size, and network bandwidth are collected.

## Running training

To execute the training stage, first initialize the environment by running the `shell_init.sh` script to install all required dependencies.

After that, execute `train_sfl_local.py` which simulates a Split Federated Learning (SFL) environment locally. You must specify the model, dataset, number of clients, quantization type, and several other parameters, which are documented in `train_sfl_local.py`.


Here is an example:

```bash
python3 train_sfl_local.py \
    --model_name VGG11 \
    --quantization_type ptq \
    --optimizer Adam \
    --dataset_name Cifar10_extreme_non_IID \
    --split_point 2 \
    --num_clients 8 \
    --image_size 224 224 \
    --client_batch_size 16 \
    --learning_rate 0.001 \
    --epochs 200
```

During training, model checkpoints are automatically saved every 10 epochs in the model-state directory.



## Running inference

Before running inference, you must configure the gRPC connection between the clients and server. After that, each device (server and clients) must have a local copy of this repository. First, run the initialization script `shell_init.sh` and then configure the environment variables.

An example of `.env` file:

```bash
CLIENT_LOCALHOST=localhost:50051,localhost:50051,localhost:50051,localhost:50051
CLIENT_ADDRESSES=client1address:50051,client2address:50051,client3address:50051,client4address:50051
MESSAGE_MAX_SIZE=400000000
AUTO_SAVE_MODELS=1
AUTO_LOAD_MODELS=1
DEBUG=0
```



```bash
python3 sfl_client.py --client_id={CLIENT_ID}
```

This will prepare the client for inference. The `{CLIENT_ID}` is used to select the data partition for that client. Each client must be numbered from 0 to the number of client minus 1.

After the setup of each client, you must run the `sfl_server.py` in the server device passing through the experiment data. Here is an example:

```bash
python3 sfl_server.py
```

the script will show some options:

```
"======== MENU ========"
"[1] - Train until accuracy reaches target"
"[2] - Quantize client model"
"[3] - Show partial test dataset accuracy
"[4] - Show full test dataset accuracy 
"[5] - Run all experiment configs
"[0] - Sair
```

To replicate the performance analysis from the thesis, choose Option [5]. This will run all the experiment configurations listened at the `experiments/inference_configs.csv` file. The raw performance metrics (latency, memory, etc.) are saved in the `./experiments/inference_results.csv` file. You can also run the `./experiments/inference_summary_results.csv` script to summarize the results. 




