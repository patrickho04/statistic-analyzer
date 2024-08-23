from Data import Data
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Preprocessing tools for machine learning
class PreprocessData(Data):
    def __init__(self, csv_file):
        super().__init__(csv_file=csv_file)
        self.dataset = np.array(self.dataset)

    def replace_missing_data(self, lower:int, upper:int) -> None:
        imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
        imputer.fit(self.dataset[:, lower:upper])
        self.dataset[:, lower:upper] = imputer.transform(self.dataset[:, lower:upper])
    
    def one_hot_encode(self, column: int) -> None:
        ct = ColumnTransformer(transformers=[('encoder', OneHotEncoder(), [column])], remainder='passthrough')
        self.dataset = np.array(ct.fit_transform(self.dataset))

    def label_encode(self, column: int) -> None:
        le = LabelEncoder()
        self.dataset[:, column] = le.fit_transform(self.dataset[:, column])
    
    def split_train_test(self) -> None:
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(self.dataset[:, :-1], self.dataset[:, -1], test_size=0.2, random_state=1)
    
    def standardize(self, list: str, lower: int, upper: int=None) -> None:
        if list not in ('x', 'y'):
            raise ValueError("Invalid option. Choose between x or y.")
        
        sc = StandardScaler()

        if list == 'x':
            if upper == None:
                self.x_train[:, lower:] = sc.fit_transform(self.x_train[:, lower:])
                self.x_test[:, lower:] = sc.transform(self.x_test[:, lower:])
            else:
                self.x_train[:, lower:upper] = sc.fit_transform(self.x_train[:, lower:upper])
                self.x_test[:, lower:upper] = sc.transform(self.x_test[:, lower:upper])
        else:
            if upper == None:
                self.y_train[:, lower:] = sc.fit_transform(self.y_train[:, lower:])
                self.y_test[:, lower:] = sc.transform(self.y_test[:, lower:])
            else:
                self.y_train[:, lower:upper] = sc.fit_transform(self.y_train[:, lower:upper])
                self.y_test[:, lower:upper] = sc.transform(self.y_test[:, lower:upper])
