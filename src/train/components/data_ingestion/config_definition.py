from collections import namedtuple

DataIngestionConfig = namedtuple("DataIngestionConfig", ["data_ingestion_dir_path",
                                                         "ingested_data_dir",
                                                         "train_file_path",
                                                         "test_file_path",
                                                         "feature_store_dir",
                                                         "feature_store_file_path",
                                                         "train_test_split_ratio",
                                                         "table_name"
                                                         ])