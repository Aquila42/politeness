for i in *_a.txt;
do mv $i ${i%%_a.txt}.txt;
done
for i in *_b.txt;
do mv $i ${i%%_b.txt}.txt;
done
