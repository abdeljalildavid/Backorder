import pandas as pd
from deepchecks.core import CheckResult, ConditionCategory, ConditionResult
from deepchecks.tabular import TrainTestCheck , Context

class ColumnsExistCheck(TrainTestCheck):
    """Check if the required columns exist in both train and test datasets."""
    
    def __init__(self, required_columns, **kwargs):
        super().__init__(**kwargs)
        self.required_columns = required_columns

    def run_logic(self, context: Context) -> CheckResult:
        # Get train and test datasets
        train_df: pd.DataFrame = context.train.data
        test_df: pd.DataFrame = context.test.data
        
        # Check for missing columns in train and test datasets
        missing_train_columns = [col for col in self.required_columns if col not in train_df.columns]
        missing_test_columns = [col for col in self.required_columns if col not in test_df.columns]
        status = True if missing_test_columns or missing_test_columns else  False
        # Prepare result value
        result_value = {
            'status' : status,
            'missing_in_train': missing_train_columns,
            'missing_in_test': missing_test_columns
        }

        # Display result in table format
        display_df = pd.DataFrame({
            'Required Columns': self.required_columns,
            'Missing in Train': [col in missing_train_columns for col in self.required_columns],
            'Missing in Test': [col in missing_test_columns for col in self.required_columns]
        })

        return CheckResult(result_value, display=[display_df])

    # Optional: Add condition to trigger an alert if any columns are missing
    def add_condition_no_missing_columns(self):
        def condition(result):
            total_missing = len(result['missing_in_train']) + len(result['missing_in_test'])
            category = ConditionCategory.PASS if total_missing == 0 else ConditionCategory.FAIL
            message = f"Found {total_missing} missing columns across train and test datasets"
            return ConditionResult(category, message)

        name = "No missing columns in both train and test datasets"
        return self.add_condition(name, condition)


