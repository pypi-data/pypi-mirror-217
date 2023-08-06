<!-- HEADER -->
|  |  |
|---|---|
| <img src="https://www.ieseg.fr/wp-content/uploads/IESEG-Logo-2012-rgb.jpg" alt="drawing" width=100%/> | <span><br>Credit Scoring<br>Module<br>Class: 2022 & 2023</span> |

<!-- CONTENT -->

---

## Overview

- Odds based Grouping (OBG)
    - OBGEncoder

        - `pred_var`: Name of predictor variable. Values can be either continuous or categorical.
        - `target_var`: Name of binary target variable.

        .fit

        - `df`: DataFrame containing pred_var and target_var.
        - `max_delta`: max difference between odds for merging two levels. default: 0.05
        - `min_bins`: minimum number of bins. default: 3
        - `q`: number of quantiles when converting continuous variable to categorical. default: 10

        .transform

        - `df`: Transform pred_var based on fitted bins.
        - `impute`: Boolean indicating whether to impute missing values. default: False
        - `impute_value`: Category level to impute missing values with. default: 'Missing' or 'nan'

        .fit_transform

        - `df`: DataFrame containing pred_var and target_var. Transform pred_var based on fitted bins.

        >fit_dict: dictionary containing the matched category levels and fitted bins.

        >lookup: dictionary containing cutoff values for continuous variable (empty if pred_var is categorical).



- Weight of Evidence (WOE)

    - WOEEncoder

        - `pred_var`: Name of predictor variable.Values can be either continuous or categorical.
        - `target_var`: Name of binary target variable. 
        - `target_value`: Value indicating event. default: 1.

        .fit

        - `df`: DataFrame containing pred_var and target_var.
        - `stop_limit`: Stops WOE based merging of the predictor's classes/levels in case the resulting information value (IV) decreases more than (e.g. 0.05 = 5%) compared to the preceding binning step. stop_limit=0 will skip any WOE based merging. Increasing the stop_limit will simplify the binning solution and may avoid overfitting. Accepted value range: 0 to 0.5. default: 0.1.
        - `q`: number of quantiles when converting continuous variable to categorical. default: 10

        .transform

        - `df`: Transform pred_var based on fitted bins
        - `impute`: Boolean indicating whether to impute missing values. default: False
        - `impute_value`: Category level to impute missing values with. default: 'Missing' or 'nan'

        .fit_transform

        - `df`: DataFrame containing pred_var and target_var. Transform pred_var based on fitted bins.

        .test_limit

        - `df`: DataFrame containing pred_var and target_var to test stop limits at 1%, 2.5%, 5% and 10%.

        >fit_dict: dictionary containing the matched category levels and fitted bins.

        >lookup: dictionary containing cutoff values for continuous variable (empty if pred_var is categorical).

<br>
