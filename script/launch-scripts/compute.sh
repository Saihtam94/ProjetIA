PYTHON_LAUNCHER='py'
cd ../
$PYTHON_LAUNCHER ReadingMessages.py
$PYTHON_LAUNCHER SplitData.py
cd data-scripts

$PYTHON_LAUNCHER PredictWithAdaboost.py
$PYTHON_LAUNCHER PredictWithDecisionTree.py
$PYTHON_LAUNCHER PredictWithKnn.py
#$PYTHON_LAUNCHER PredictWithLogisticRegression.py
$PYTHON_LAUNCHER PredictWithNB.py
$PYTHON_LAUNCHER PredictWithRandomForest.py
$PYTHON_LAUNCHER PredictWithSvm.py