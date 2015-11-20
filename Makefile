problem1: prob1.py
	python prob1.py > prob1.dot
	dot -Tpng -oprob1.png prob1.dot
	open prob1.png

problem2: prob2.py
	python prob2.py > prob2.dot
	dot -Tpng -oprob2.png prob2.dot
	open prob2.png

clean:
	rm *.pyc
	rm *.png
	rm *.dot
