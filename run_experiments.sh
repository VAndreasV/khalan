#!/bin/bash
echo Started experiments...

#python main.py -g 100 -a2 mcts &
#python main.py -g 100 -a2 rave &
#python main.py -g 100 -a2 ucrave &

#python main.py -g 100 -a1 mcts -sa1 100 -a2 mcts -sa2 1000 &
#python main.py -g 100 -a1 mcts -sa1 100 -a2 mcts -sa2 100 -UCBC2 2 &
#python main.py -g 100 -a1 mcts -sa1 100 -a2 mcts -sa2 100 -UCBC2 0.5 &
python explore.py -g 100 -p c -min 0.0 -max 1.5 -s 0.05 -p1_strategy mcts -p2_strategy rave &


#python main.py -g 100 -a1 rave -sa1 100 -a2 rave -sa2 1000 &
python explore.py -g 100 -p k -min 0.0 -max 1.0 -s 0.05 -p1_strategy rave -p2_strategy mcts &

python explore.py -g 100 -p k -min 0.0 -max 1.0 -s 0.05 -p1_strategy ucrave -p2_strategy mcts &
python explore.py -g 100 -p c -min 0.0 -max 1.5 -s 0.05 -p1_strategy ucrave -p2_strategy mcts &

#wait

#python main.py -g 100 -a1 ucrave -sa1 100 -a2 ucrave -sa2 1000 &
#python main.py -g 100 -a1 ucrave -sa1 100 -a2 ucrave -sa2 100 -RAVEK2 0.8 &
#python main.py -g 100 -a1 ucrave -sa1 100 -a2 ucrave -sa2 100 -RAVEK2 0.2 &
#python main.py -g 100 -a1 ucrave -sa1 100 -a2 ucrave -sa2 100 -UCBC2 2 &
#python main.py -g 100 -a1 ucrave -sa1 100 -a2 ucrave -sa2 100 -UCBC2 0.5 &



wait
echo All DONE