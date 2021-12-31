rm output/*
rm output/.*
rmdir output
./run-local.sh output -gs.input yeast_s2_edge -gs.sf 2
python combine.py output yeast_s4_edge