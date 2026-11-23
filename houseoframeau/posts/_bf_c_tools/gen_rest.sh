#!/bin/bash
# voice the other four posts one after another once PURCELL's voice is done (one Chatterbox at a time: 4 cores)
cd /home/user/Mymobileworld/houseoframeau/posts
until [ -f bf-purcell/vo/L7.wav ]; do sleep 5; done; sleep 5
while pgrep -f "vo.py gen bf-purcell" >/dev/null; do sleep 3; done
for p in bf-jiyu-nad bf-luvum bf-momo-nashi bf-manners; do ~/.presenter-tools/cbx/bin/python -I _bf_c_tools/vo.py gen $p 2>&1 | grep -E "VO_OK|Error|Traceback"; done
echo GEN_REST_DONE
