#!/bin/bash

#SBATCH --job-name=tiger
#SBATCH --partition=gpu-4080     # 指定分区为cpu-13900,gpu-4080
#SBATCH --nodelist=               # 指定的节点名，如MW06
#SBATCH --nodes=1                    # 使用1个节点
#SBATCH --ntasks-per-node=1          # 每个节点上运行的任务数
#SBATCH --cpus-per-task=8            # 每个任务分配的CPU核心数
#SBATCH --mem=2G                     # 分配的内存
#SBATCH --time=2000:00:00              # 任务运行的最大时间 (500小时)
#SBATCH --output=output/job_output_%j.txt   # 输出文件
#SBATCH --error=output/job_error_%j.txt     # 错误文件

# 加载你需要的模块（如果有的话，例如某些软件或库）
# module load some_module

# 进入提交脚本所在的目录
cd "$SLURM_SUBMIT_DIR"

# 运行你的命令或脚本

python allsort.molg 
python allsort.py 
python draw_all_variables.py
python draw_cluster.py 