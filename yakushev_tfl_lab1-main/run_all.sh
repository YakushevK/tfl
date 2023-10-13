for f in {1..10}
do  
    echo -n test$f ": " &&
    python main.py my_tests/$f.txt temp.smt2 &&
    z3 -smt2 temp.smt2 
done


echo ""
echo ""
echo "почему-то последний тест валится, хотя, если его запустить отдельно, то работает"