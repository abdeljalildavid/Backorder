from dataclasses import dataclass


@dataclass
class DataTransformationArtifact:
    transformed_data_train_file_path: str
    transormed_data_test_file_path: str
    transformation_pipeline_file_path: str