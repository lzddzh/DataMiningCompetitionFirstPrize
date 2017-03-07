#!/bin/sh
rm testProcessed/collumInfo.txt
cp testProcessed/examples_test.txt_backup testProcessed/examples_test.txt
python tool.py add BorrowProcessed.txt normalization=$1 test
python tool.py add DormProcessed.txt normalization=$1 test
python tool.py add LibraryProcessed.txt normalization=$1 test
python tool.py add ScoreProcessed.txt normalization=$1 test
python tool.py add Card2Processed.txt normalization=$1 test
python tool.py add Card3Processed.txt normalization=$1 test
python tool.py add FacultyProcessed.txt normalization=$1 test
python tool.py add RankProcessed.txt normalization=$1 test
python standardization.py test std
python add_head.py testProcessed/examples_test_std.txt testProcessed/idexamples_test_std.txt 
python add_head.py trainProcessed/examples_train_std.txt trainProcessed/idexamples_train_std.txt
