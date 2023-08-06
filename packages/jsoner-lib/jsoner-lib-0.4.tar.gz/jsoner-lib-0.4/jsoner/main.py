import os
import json
from pydantic import BaseModel


class Jsoner:
    """
        A class for saving arbitrary data models to a json file
        :param models: list of model that will be saving 
        :param filename: name of file where will be saving data
        :param save_immediately: if true: saving will start after every append
    """
    def __init__(
            self,
            models: list[BaseModel] | BaseModel,
            filename: str,
            save_immediately: bool = False):
        
        self.models = models
        if not filename.endswith(".json"):
            raise ValueError("You should use only json files")
        
        self.filename = filename
        self.save_immediately = save_immediately

        self.objects_to_save = []

    def _belong_to_models(self, obj: BaseModel) -> bool:
        """
            Check if model is instance of some model from self.models
            :param obj: Object of some model
        """
        for m in self.models:
            if isinstance(obj, m):
                return True
        return False
    
    def append(self, obj: BaseModel) -> None:
        """
            Add object to list of objects
            :param obj: Object of some model
        """
        if not self._belong_to_models(obj):
            raise ValueError("You can't use underfinded models")
        self.objects_to_save.append(obj.dict())

        if self.save_immediately:
            self.save()

    def _get_json_from_file(self) -> dict | None:
        """
            Extract data from json file to python dict 
            :return data: dict from json file or None
        """
        if not os.path.exists(self.filename):
            return None
        
        with open(self.filename, "r") as file:
            file = file.read()
            if not file:
                return None
            data = json.loads(file)

        return data

    def save(self, indent: int = 4, ensure_ascii: bool = True, allow_nan: bool = True):
        """
            Save objects to json file
            params equal to json.dump params
        """
        jsn = self._get_json_from_file()
        with open(self.filename, "w") as file:
            if isinstance(jsn, list):
                jsn.extend(self.objects_to_save) if jsn else None

            if isinstance(jsn, dict):
                jsn.update(self.objects_to_save) if jsn else None

            jsn = jsn if jsn else self.objects_to_save
            json.dump(jsn, file, indent=indent, ensure_ascii=ensure_ascii, allow_nan=allow_nan)
