from collections import namedtuple

DataValidationConfig = namedtuple("DataValidationConfig", [
                                                         "data_validation_dir_path",
                                                         "valid_data_dir",
                                                         "invalid_data_dir",
                                                         "valid_train_file_path",
                                                         "valid_test_file_path",
                                                         "invalid_train_file_path",
                                                         "invalid_test_file_path",
                                                         "report_dir_path",
                                                         "drift_report_dir_path",
                                                         "drift_report_yaml_file_path",
                                                         "drift_report_html_file_path",
                                                         "missing_columns_html_file_path",
                                                         ])