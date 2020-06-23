# EEG-ERP data and machinelearning 
Classify schizophrenia and Healthy by EEG data and machinelearning algorithm. 
But it's hard to classify only with machinelearning and data so tried deeplearning model named perceptrone.
To increase accuracy, augmentation with random number between [-5.000000,5.000000] for 3 times.
Several steps are also done, such as robust scaling and increasing epoch or batch size, layers.
However, all of these did not work for data and accuracy is always 57%~62%.
Accuracy never increased..
As a result, EEG-ERP data is not appropriate for classifying schizophrenia and Healthy with machinlearning.

The bad result reason may:
  1. Too small subjects - this data only has 81 subjects.
  2. wrong measurement of EEG data.
  3. numerical EEG data is not appropriate for classification.
These three reasons are the assumption that we can do.

# Replace EEG with MRI
Beacause of the uncertainty of EEG data in classifying sz and healthy control, we used MRI dataset instead.

# MRI data and machinelearning
The specification of MRI dataset:
  1. Subjects- 86, 48 for control, and 38 for sz.
  2. FNC - 378 paris of brain maps
     SBM - 74 brain maps
  3. train - 86 rows for each brain map
     test - 100,000 rows for each brain map

Several steps are done, and final acuuracy is about 92%, using Gaussian Processor(GP Toolbox).

# Local SW Program
Classification between sz and control using machinelearning is done, so based on the result, we implemented local SW program for Diagnosing the patient whether she/he is sz or not.
We used Python, under virtual environment with conda, and MNE library for EEG waves visualization.
