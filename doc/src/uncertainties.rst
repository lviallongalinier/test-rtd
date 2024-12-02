.. _uncertainty:

Uncertainty  and quality representation
=======================================

Let's start with definitions:

Uncertainty
    Uncertainty refers to the quantitative uncertainty defined as the 68% confidence interval on the measured value or standard deviation of various measurments (which is equivalent under the hypothesis of a normal distribution of errors).

Quality
    Quality is a qualitative indication on the uncertainty on measurement compared to the typical uncertainty of the method used. We use a 4 level scale:

    - Good: reliable data within the standard quality of the method
    - Uncertain: data whose quality is probably below the standard quality of the method (doubts in the measurement or data processing procedure).
    - Low quality: data whose quality is undoubtedly below the standard quality of the method due to measurements or data processing procedure.
    - Bad: undoubtedly erroneous data

    As soon as the level is not set to "Good" (which is assumed if no provided), some additional details should be provided in the associated profile comment.


Uncertainties on various metadatas
----------------------------------

Uncertainties at profile level
------------------------------

For each profile, it is possible to associate an uncertainty and a quality flag that will apply to the whole profile. Keys ``uncertainty_of_measurement`` and ``quality_of_measurement`` are generally used. The quality and uncertainty then apply to the whole profile.

The uncertainty field should NOT be filled the uncertainty corresponds to the standard uncertainty of the measurement method. It could be filled when it brings an added value compared to the typical value of the measurement method. This can be the case if special sampling conditions lead to an increased uncertainty or if it has been measured (by doing multiples sampling for instance) for instance.

Uncertainties at measurement level
----------------------------------

When uncertainty or quality of measurement varies significantly between the different layer or points of the snowpack, both uncertainty and quality could be specified in the ``data`` table directly at the layer or point level with keys ``uncertainty`` or ``quality``. If all the values are similar, then you should probably use uncertainties at profile level.
