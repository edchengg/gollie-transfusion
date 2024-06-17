#!/bin/bash
#SBATCH --job-name=tf
#SBATCH --output=tf_%a_%j.out
#SBATCH --error=tf_%a_%j.err
#SBATCH --partition="nlprx-lab"
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=24
#SBATCH --gpus-per-node="a40:4"
#SBATCH --qos="short"
#SBATCH --exclude="heistotron,puma,omgwth,cheetah"
#SBATCH -a 1-100
#SBATCH --requeue

# Training
python3 -m src.run configs/model_configs/gollie-tf.yaml

# Inference
DATASET_PATH=GoLLIE/data/processed_w_examples/tfv1_test #Set dataset path
DATASET_NAME=masakhaner,massive
NUM_SIZE=200
OUTPUT_PATH=GoLLIE/model_output/gollie_tf #Set model path
LORA_PATH=GoLLIE/model_output/gollie_tf #Set lora path

python3 -m src.hf_inference --dataset_path $DATASET_PATH --task_name_list $DATASET_NAME --num_size $NUM_SIZE --output_path $OUTPUT_PATH --lora_path $LORA_PATH --use_lora --batch_size 8