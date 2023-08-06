import numpy as np
from arch import arch_model

"""
Parametric bootstrapping with GARCH models.
"""

class Garch:
    
    def __init__(self, data, vol='Garch', p=1, q=1, dist='normal', update_freq=0, disp='off', horizon=1, start=None, reindex=False):
        
        """
        Initializing the GARCH model.

        Parameters:
        ---------------
            data: pandas.Series
                Time series data
            vol: str, optional
                Name of the volatility model. Default is 'Garch'. Others are 'ARCH', 'EGARCH', 'FIGARCH', 'APARCH' and 'HARCH'
            p: int, optional
                Lag order of the symmetric innovation. Default is 1.
            q: int
                Lag order of the lagged conditional variance. Default is 1.
            dist: str, optional
                Name of the distribution assumption for the errors. Options are:
                    * Normal: 'normal', 'gaussian' (default)
                    * Students's t: 't', 'studentst'
                    * Skewed Student's t: 'skewstudent', 'skewt'
                    * Generalized Error Distribution: 'ged', 'generalized error"
            update_freq: int, optional
                Frequency of iteration updates to generate model output. Default is 0 (no updating).
            disp: str or bool optional
                Display option for the model estimation. Either 'final' to print optimization result or 'off' (default) to display
                nothing. If using a boolean, False is "off" and True is "final"
            horizon: int, optional
                Forecast horizon. Default is 1.
            start: int or str or datetime or Timestamp, optional
                Starting index or date for forecasting. Default is None.
            reindex: bool, optional
                Reindex the forecasted series to match the original data. Default is False.
        """

        # Store the model parameters
        self.vol = vol
        self.p = p
        self.q = q
        self.dist = dist
        self.horizon = horizon

        # Call the model
        self.model = arch_model(data, vol=self.vol, p=self.p, q=self.q, dist=self.dist)
        # Fit the model
        self.result = self.model.fit(disp=disp)
        # Forecast
        self.prediction = self.result.forecast(horizon=self.horizon, start=start, reindex=reindex)

    @property
    def summary(self):
        """
        Get the summary of the fitted GARCH model.

        Returns:
        ------------
            arch.univariate.base.ARCHModelResultSummary: Summary of the fitted model.
        """
        
        return self.result.summary()
    
    @property
    def conditional_volatility(self):
        """
        Get the conditional volatility of the fitted GARCH model.

        Returns:
        ------------
            pandas.Series: Conditional volatility series.
        """
        
        return self.result.conditional_volatility
    

    @property
    def standardised_residuals(self):
        """
        Get the standardized residuals of the fitted GARCH model.

        Returns:
        ------------
            pandas.Series: Standardized residuals series.
        """
        return self.result.std_resid


    @property
    def forecast_mean(self):
        """
        Get the forecasted conditional mean of the GARCH model.

        Returns:
        ------------
            pandas.DataFrame: Forecasted conditional mean series.
        """
        return self.prediction.mean
    

    @property
    def forecast_variance(self):
        """
        Get the forecasted conditional variance of the GARCH model.

        Returns:
        ------------
            pandas.DataFrame: Forecasted conditional variance series.
        """
        return self.prediction.variance
    

    @property
    def forecast_residual_variance(self):
        """
        Get the forecasted conditional variance of the residuals of the GARCH model.

        Returns:
        ------------
            pandas.DataFrame: Forecasted conditional residual variance series.
        """
        return self.prediction.residual_variance
    
#-------------------------------------------------------------------------------------------
    
    def bootstrap(self, num_iterations=1000):
        
        """
        Perform parametric bootstrapping to estimate the forecast distribution.

        Parameters:
        ------------
            num_iterations: int, optional
                Number of bootstrap iterations. Default is 1000.

        Returns:
        ------------
            bool: True if the bootstrap is successful.
        """
        
        # Getting the standardised residuals
        std_resid = self.standardised_residuals
        
        # Empty list to store the mean and volatility forecast
        bootstrap_samples = []
        
        # Paramteric Bootstrapping
        for _ in range(num_iterations):
            
            # Resampling the std residuals
            bootstrap_residuals = std_resid.sample(n=len(std_resid), replace=True)
            
            # Fit the GARCH model to the bootstrap sample
            bootstrap_model = arch_model(
                bootstrap_residuals,
                vol=self.vol,
                p=self.p,
                q=self.q,
                dist=self.dist
            )            
            
            bootstrap_result = bootstrap_model.fit(disp='off') 
            
            # Calculate mean and volatility forecast for the desired horizon
            forecasted_mean = bootstrap_result.forecast(horizon=self.horizon, start=None, reindex=False).mean
            forecasted_volatility = bootstrap_result.forecast(horizon=self.horizon, start=None, reindex=False).variance
    
            # Append forecasted mean and volatility to empty list
            bootstrap_samples.append((forecasted_mean, forecasted_volatility))
        
        # Assign bootstrap_samples and bootstrap_result to the property
        self._bootstrap_samples = bootstrap_samples
        self.bootstrap_result = bootstrap_result

        return True


    @property
    def bootstrap_summary(self):
        """
        Get the summary of the bootstrapped model.

        Returns:
        ------------
            arch.univariate.base.ARCHModelResultSummary: Summary of the bootstrapped model.
        """
        return self.bootstrap_result.summary()
    
    
    # Return the forecasted mean and volatility list
    @property
    def bootstrap_samples(self):
        """
        Get the forecasted mean and volatility list from the bootstrapped model.

        Returns:
        ------------
            list: List of tuples containing forecasted mean and volatility for each bootstrap iteration.
        """
        
        # Check if bootstrap_samples is available
        if self._bootstrap_samples is None:
            raise ValueError("Please run the 'bootstrap' method to generate bootstrap samples.")
        
        return self._bootstrap_samples
    
 
    #-------------------------------------------------------------------------------------------

    def estimate_risk(self, confidence_level=0.95):
        """
        Estimate risk measures: volatility and Value-at-Risk (VaR) using the bootstrapped model.

        Parameters:
        ------------
            confidence_level: float, optional
                Confidence level for calculating VaR and volatility. Default is 0.95.

        Returns:
        ------------
            dict: Dictionary containing risk estimates including mean volatility, volatility confidence interval,
                  mean VaR, and VaR confidence interval.
        """
        
        # Calculate the volatility
        volatility_estimates = np.sqrt([vol for _, vol in self.bootstrap_samples])

        # Volatility Confidence Interval
        volatility_ci = np.percentile(volatility_estimates, [(1 - confidence_level) / 2 * 100, (1 + confidence_level) / 2 * 100])

        # Calculate VaR using the empirical quantile method
        quantile = self.result.std_resid.quantile(1 - confidence_level)  # Set the desired quantile
        var_estimates = []

        for forecasted_mean, forecasted_volatility in self.bootstrap_samples:
            var_estimate = forecasted_mean + np.sqrt(forecasted_volatility) * quantile
            var_estimates.append(var_estimate)

        # Calculate the mean VaR estimate
        mean_var = np.mean(var_estimates)

        # VaR Confidence Interval
        var_ci = np.percentile(var_estimates, [(1 - confidence_level) / 2 * 100, (1 + confidence_level) / 2 * 100])

        return {
            'Mean Volatility': np.mean(volatility_estimates),
            'Volatility Confidence Interval': volatility_ci,
            'Mean VaR': mean_var,
            'VaR Confidence Interval': var_ci
        }
