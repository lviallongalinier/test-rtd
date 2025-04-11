.. _uncertainty:

Describe data uncertainty and quality 
=====================================

The package allows to describe a quantitative uncertainty and/or a quality flag of the data. They can be assigned to the whole profile, to specific layers or heights of the profile, or to metadata.

Uncertainty
    Uncertainty refers to the quantitative uncertainty of the measured values, defined as the 68% confidence interval or the measurement standard deviation (which is equivalent under the hypothesis of a normal distribution of errors).
    
    The uncertainty field should not be filled by the standard, published uncertainty of the measurement method. It can be filled in when it differs from the standard uncertainty of the measurement method. For example, in the case of specific sampling conditions which may lead to a variation in measurement uncertainty, or if a standard deviation has been specifically estimated using several repeated measurements.

Quality
    Quality is a qualitative indication of the quality of the measured values, compared with the standard quality expected for that measurement. We use a 4-level scale:
    
    - Good: reliable data, conforming to the standard quality of the method
    - Uncertain: data whose quality is probably below the standard quality of the method (in case of doubts in the measurement and/or data processing procedure).
    - Low quality: data whose quality is undoubtedly lower than the standard quality of the method.
    - Bad: data undoubtedly erroneous.
    
    If not set to "Good", additional details should be provided in the associated profile comment.


Uncertainties on various metadata
----------------------------------
Uncertainty and quality flag can be assigned to some metadata. 


Uncertainties over an entire profile
------------------------------------

Uncertainty and quality flag can be assigned to an entire profile. Keys ``uncertainty_of_measurement`` and ``quality_of_measurement`` are generally used.


Uncertainties on a data point or layer
--------------------------------------

Uncertainty and quality flag can be defined for specific layers or for specific heights of the profile. 
For example, it can be used to describe higher uncertainties or lower quality due to the difficulty of sampling in a specific area of the snowpack.
The keys ``uncertainty`` or ``quality`` can be filled for the considered layer or height in the ``data`` table.

 
 
 
 
 
 
 
 
 
