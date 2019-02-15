#!/bin/bash

python preprocess.py --sample 20;
python fit.py --sample 20;

python preprocess.py --sample 30;
python fit.py --sample 30;

python preprocess.py --sample 40;
python fit.py --sample 40;

python preprocess.py --sample 50;
python fit.py --sample 50;

python preprocess.py --sample 60;
python fit.py --sample 60;

python preprocess.py --sample 70;
python fit.py --sample 70;

python preprocess.py --sample 80;
python fit.py --sample 80;
python preprocess.py --sample 100;
python fit.py --sample 100;




