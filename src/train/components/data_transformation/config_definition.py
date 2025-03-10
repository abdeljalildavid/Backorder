from collections import namedtuple

DataTransformationConfig = namedtuple("DataTransformationConfig",
                                   [
                                     "data_transformation_dir_path",
                                     "transformed_data_dir_path",
                                     "transformed_train_data_file_path",
                                     "transformed_test_data_file_path",
                                     "transfarmation_pipeline_object_dir_path",
                                     "transfarmation_pipeline_object_file_path"

                                    ])