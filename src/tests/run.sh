python test.py f1.txt 101
echo "Expected: Aceita"

python test.py f1.txt 100
echo "Expected: Não aceita"

python test.py f2.txt 111
echo "Expected: Aceita"

python test.py f2.txt 101
echo "Expected: Não aceita"

python test.py f3.txt 101
echo "Expected: Aceita"

python test.py f3.txt 10
echo "Expected: Não aceita"