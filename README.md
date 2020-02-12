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
