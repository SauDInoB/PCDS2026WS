

# Pearson correlation coefficient
“r = pearsonr(mydata['x'],mydata['y']);
     print("Pearson correlation: ")
     print(r,'\n')”


# Simple linear regression


“     mydata = pd.read_csv(url)   # save as mydata file
     print(mydata.head(10))
     sns.regplot(data=mydata,x='Packs',y='Longevity')
 
     r = pearsonr(mydata['Packs'],mydata['Longevity']);
     print("\nPearson corelation: ")
     print(r,'\n')
 
     # fit simple linear regression model
     linear_model = ols('Longevity ~ Packs', data=mydata).fit()
     print(linear_model.summary())”

Excerto de
Applied Statistics with Python: Volume I: Introductory Statistics and Regression
Kaganovskiy, Leon
É possível que este material esteja protegido por copyright.

“plt.figure(figsize=(7,5))
     import lmdiag
     lmdiag.plot(linear_model);”

Excerto de
Applied Statistics with Python: Volume I: Introductory Statistics and Regression
Kaganovskiy, Leon
É possível que este material esteja protegido por copyright.

# “xs =np.linspace(0, 7, num=8)
     predictions = linear_model.get_prediction(pd.DataFrame({'Packs':xs}))
     df = pd.DataFrame(predictions.summary_frame(alpha=0.05))
     df.insert(loc=0, column='xs', value=xs); df”

Excerto de
Applied Statistics with Python: Volume I: Introductory Statistics and Regression
Kaganovskiy, Leon
É possível que este material esteja protegido por copyright.

“xs = 5; yexact = 60; b = linear_model.params; ys = b[0] + b[1]*xs;
     print('xs = {:.3f}, ys = {:.3f}, yexact = {:.3f}, residual = {:.3f}'.
           format(xs,ys,yexact,yexact-ys))
     se = np.sqrt(linear_model.scale);
     print('Residual standard error = se = {:.3f}'.format(se))”

Excerto de
Applied Statistics with Python: Volume I: Introductory Statistics and Regression
Kaganovskiy, Leon
É possível que este material esteja protegido por copyright.

# Simple linear regression with categorical predictor

“# import packages and libraries
     import numpy as np; import pandas as pd
     import matplotlib.pyplot as plt; import seaborn as sns;
     import statsmodels.api as sm; from scipy.stats import pearsonr
     from statsmodels.formula.api import ols
 
     url="https://raw.githubusercontent.com/leonkag/Statistics0/main/HELPrct.csv"
     mydata = pd.read_csv(url)   # save as mydata file
     # print(mydata.head(10))
     sns.boxplot(data=mydata,x='sex',y='cesd')
 
     # fit simple linear regression model
     linear_model = ols('cesd ~ sex', data=mydata).fit()
     print(linear_model.summary())
     print('\nHigher accuracy printout of p-values: \n',linear_model.pvalues,'\n')”

Excerto de
Applied Statistics with Python: Volume I: Introductory Statistics and Regression
Kaganovskiy, Leon
É possível que este material esteja protegido por copyright.

“from scipy import stats
     stats.ttest_ind(mydata[mydata['sex']=='female']['cesd'],
                     mydata[mydata['sex']=='male']['cesd'], equal_var=True)”

Excerto de
Applied Statistics with Python: Volume I: Introductory Statistics and Regression
Kaganovskiy, Leon
É possível que este material esteja protegido por copyright.

“# import packages and libraries
      import numpy as np; import pandas as pd
      import matplotlib.pyplot as plt; import seaborn as sns;
      import statsmodels.api as sm; from scipy.stats import pearsonr
      from statsmodels.formula.api import ols
 
      url="https://raw.githubusercontent.com/leonkag/Statistics0/main/HELPrct.csv"
      mydata = pd.read_csv(url)   # save as mydata file
      # print(mydata.head(10))
      sns.boxplot(data=mydata,x='substance',y='cesd')”

Excerto de
Applied Statistics with Python: Volume I: Introductory Statistics and Regression
Kaganovskiy, Leon
É possível que este material esteja protegido por copyright.
“# fit simple linear regression model
      linear_model = ols('cesd ~ substance', data=mydata).fit()
      print(linear_model.summary())
      print('\nHigher accuracy printout of p-values: \n',linear_model.pvalues,'\n')”

Excerto de
Applied Statistics with Python: Volume I: Introductory Statistics and Regression
Kaganovskiy, Leon
É possível que este material esteja protegido por copyright.