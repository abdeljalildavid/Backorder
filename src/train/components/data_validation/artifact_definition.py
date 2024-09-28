from dataclasses import dataclass


@dataclass
class DataValidationArtifact:
    #validation_status: bool
    valid_train_file_path: str
    valid_test_file_path: str
    invalid_train_file_path: str
    invalid_test_file_path: str
    drift_report_yaml_file_path: str