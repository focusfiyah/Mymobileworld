while pgrep -f "twin-shorts/work/task.yaml" >/dev/null; do sleep 20; done
cd /root/.ram-tools/musetalk/src && OMP_NUM_THREADS=4 ../venv/bin/python -m scripts.inference --inference_config /home/user/Mymobileworld/ralph/twin-shorts/work/flow/task.yaml --result_dir /home/user/Mymobileworld/ralph/twin-shorts/work/flow/mt --unet_config models/musetalkV15/musetalk.json --version v15 --ffmpeg_path /usr/bin --saved_coord --batch_size 4 > /tmp/mt_flow.log 2>&1
echo FLOW_MT_DONE >> /tmp/mt_flow.log
