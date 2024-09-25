from deepchecks.core import CheckResult
from deepchecks.core.checks import BaseCheck

class ColumnsExistCheck(BaseCheck):
    def __init__(self, required_columns, **kwargs):
        super().__init__(**kwargs)
        self.required_columns = required_columns

    def run(self, dataset):
        missing_columns = [col for col in self.required_columns if col not in dataset.columns]
        
        if missing_columns:
            return CheckResult(
                value={"missing_columns": missing_columns},
                success=False,
                display="Some columns are missing!"
            )
        else:
            return CheckResult(
                value={"missing_columns": None},
                success=True,
                display="All required columns are present!"
            )


