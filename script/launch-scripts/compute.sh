PYTHON_LAUNCHER='py'
cd ../
$PYTHON_LAUNCHER ReadingMessages.py
$PYTHON_LAUNCHER SplitData.py
cd data-scripts
$PYTHON_LAUNCHER PredictWithKnn.py
$PYTHON_LAUNCHER PredictWithNB.py
$PYTHON_LAUNCHER PredictWithSvm.py