# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * #
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * #
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * #
# * * * * *                                                                     * * * * * #
# * * * * *                                                                     * * * * * #
# * * * * *     Comparison of Conversion of Bidding Methods with AB Testing     * * * * * #
# * * * * *                                                                     * * * * * #
# * * * * *                                                                     * * * * * #
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * #
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * #
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * #

#####################################################
# Business Case
#####################################################
# Facebook recently introduced a new bidding type, 'average bidding',
# as an alternative to the existing bidding type called 'maximum bidding'.
# One of our clients, bombabomba.com, decided to test this new feature and would like to run an A/B test
# to see if average bidding converts more than maximum bidding.
# The A/B test has been going on for 1 month and now bombabomba.com is waiting for you
# to analyze the results of this A/B test.
# The ultimate success criterion for Bombabomba.com is Purchase.
# Therefore, the focus should be on the Purchase metric for statistical testing.

#####################################################
# Story of the Dataset
#####################################################

# In this data set, which includes the website information of a company,
# there is information such as the number of advertisements that users see and click,
# as well as earnings information from here.
# There are two separate data sets, the control and test groups.
# These datasets are in separate sheets of the ab_testing.xlsx excel.
# Maximum Bidding was applied to the control group and Average Bidding was applied to the test group.

#####################################################
# Variables
#####################################################
# Impression: Views count of Ad
# Click: Number of clicks on the displayed ad
# Purchase: Number of products purchased after ads clicked
# Earning: Earnings after purchased products

#####################################################
# PROJECT TASKS
#####################################################

import pandas as pd

from scipy.stats import shapiro, levene, ttest_ind

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 750)
pd.set_option('display.precision', 4)
# ---
# 1. **Data Prep and Analyse**
#   1. Read the data set ab_testing_data.xlsx consisting of control and test group data.
#   Assign control and test group data to separate variables
df_control = pd.read_excel("datasets/ab_testing.xlsx", sheet_name="Control Group")
df_test = pd.read_excel("datasets/ab_testing.xlsx", sheet_name="Test Group")

#   2. Analyse control and test group data.
df_control.head()
df_test.head()
df_control.shape  # 40,4
df_test.shape  # 40,4
df_control.describe().T
df_test.describe().T
df_control.isnull().sum()
df_test.isnull().sum()


def compare_var_sums(df1, df2):
    for col in df1.columns:
        sum1 = df1[col].sum()
        sum2 = df2[col].sum()
        if sum1 > sum2:
            print(f"Sum of {col} in df1 is more")
        elif sum1 == sum2:
            print(f"Sum of {col} in df1 and df2 is equal")
        else:
            print(f"Sum of {col} in df1 is less")


compare_var_sums(df_control, df_test)
"""
Sum of Impression in df1 is less
Sum of Click in df1 is more
Sum of Purchase in df1 is less
Sum of Earning in df1 is less
"""
#   3. After analyse process, merge control and test group using concat method
df = pd.concat([df_control.add_suffix('_Control'), df_test.add_suffix('_Test')], axis=1)
df.head()
df
df.shape  # 80, 4 as expected
# ---
# 2. **Defining the AB Test Hypothesis**
#    1. Define the hypothesis.
#    <br>
#    H0 : M1 = M2
#    <br>
#    H1 : M1!= M2
"""
------------------
# ANSWERS:
------------------
# H0: There is NO statistically meaningful difference between "Average Bid" and "Maximum Bid" in purchasing averages.
# H1: There IS statistically meaningful difference between "Average Bid" and "Maximum Bid" in purchasing averages.
"""

#   2. Analyze the purchase averages for the control and test group.

list(df.columns)  # Purchase_Control, Purchase_Test are the vars we need
df[["Purchase_Control", "Purchase_Test"]].mean()

# ---
# 3. **Performing Hypothesis Testing**
#    1. Perform hypothesis checks before hypothesis testing
"""
-----------------------------
#    Normality Assumption:
-----------------------------
"""
# H0: Normal Distribution Assumption is Valid
# H0: Normal Distribution Assumption is NOT Valid
# If Normality is not valid then go to Non-parametric Test

# PURCHASE CONTROL - Maximum Bidding
test_stat, p_value = shapiro(df["Purchase_Control"])
print("Test Stat = %.4f, p-value = %.4f" % (test_stat, p_value))
# Test Stat = 0.9773, p-value = 0.5891
# p-value > 0.05, H0 cannot be rejected. -> Purchase_Control is Normally distributed
# ------------------------------------------
# PURCHASE TEST - Average Bidding
test_stat, p_value = shapiro(df["Purchase_Test"])
print("Test Stat = %.4f, p-value = %.4f" % (test_stat, p_value))
# Test Stat = 0.9589, p-value = 0.1541
# p-value > 0.05, H0 cannot be rejected. -> Purchase_Test is Normally distributed
# ------------------------------------------
"""
-----------------------------
#    Variance Homogeneity:
-----------------------------
"""
# H0: Variances are homogeneous
# H1: Variances are NOT homogeneous
test_stat, p_value = levene(df["Purchase_Control"], df["Purchase_Test"])
print("Test Stat = %.4f, p-value = %.4f" % (test_stat, p_value))
# Test Stat = 2.6393, p-value = 0.1083
# p-value > 0.05, H0 cannot be rejected. -> Variances are homogeneous
# ------------------------------------------
#    2. Select the appropriate test according to the Normality Assumption and Variance Homogeneity results
"""
All the assumptions are valid. So we'll go with the parametric test
"""
test_stat, p_value = ttest_ind(
    df["Purchase_Control"],
    df["Purchase_Test"],
    equal_var=True  # Variance homogeneity is valid, equal_var=True
)
print("Test Stat = %.4f, p-value = %.4f" % (test_stat, p_value))
# Test Stat = -0.9416, p-value = 0.3493
"""
# p_value > 0.05, H0 cannot be rejected. ->
There is NO statistically meaningful difference between
"Average Bid" and "Maximum Bid" in purchasing averages.
"""
#    3. Considering the p_value obtained as a result of the test,
#    interpret whether there is a statistically meaningful difference
#    between the purchasing averages of the control and test groups.
"""
There is NO statistically meaningful difference between
"Average Bid" and "Maximum Bid" in purchasing averages.
We know that Test Dataset has more purchases sum than Control Dataset has.
But this is only by chance.
"""

# ---
# 4. **Analysis of Results**
#    1. Which test did you use, state the reasons.
"""
I used shapiro test for Normality Assumption to determine if data has normal distribution.
I used levene test for Variance Homogeneity to determine 
whether the variances of purchase_control/test groups are equal or not.
I used t-test(parametric), after all the p_values were above 0.05.
"""
#    2. Advise the customer according to the test results you have obtained.
"""
You use both of the bidding systems because
there is no statically meaningful relation between two bidding types.
It looks like average bidding method had more impressions, purchases and earnings 
by chance.
"""
# ---
