from attr import dataclass
from sklearn.pipeline import Pipeline

@dataclass
class Transformer:
    
    name:str
    pipeline:Pipeline
    columns :list[str]
    @property
    def transformer(self)->tuple[str,Pipeline,list[str]]:
        return (self.name,self.pipeline,self.columns)
    


@dataclass
class DatasetBalancer:
    name:str
    pipeline:Pipeline

    

