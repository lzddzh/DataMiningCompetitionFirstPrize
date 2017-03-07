#!/bin/sh
rm trainProcessed/collumInfo.txt
cp trainProcessed/examples_train.txt_backup trainProcessed/examples_train.txt
python tool.py add BorrowProcessed.txt normalization=$1 train
python tool.py add DormProcessed.txt normalization=$1 train
python tool.py add LibraryProcessed.txt normalization=$1 train
python tool.py add ScoreProcessed.txt normalization=$1 train
python tool.py add Card2Processed.txt normalization=$1 train
python tool.py add Card3Processed.txt normalization=$1 train
python tool.py add FacultyProcessed.txt normalization=$1 train
python tool.py add RankProcessed.txt normalization=$1 train
#python standardization.py train std 
#python add_head.py trainProcessed/examples_train_std.txt trainProcessed/idexamples_train_std.txt
