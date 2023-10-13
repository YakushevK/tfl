python main.py $1 temp.smt2 &&

echo && 
echo "FILE:" && 
cat $1 &&

echo &&
echo &&
echo "GENERATED:" &&
cat temp.smt2 &&

echo &&
echo &&
echo "RESULT:" &&
z3 -smt2 temp.smt2 