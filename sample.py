import abc
import json
from tinydb import TinyDB, Query
 
class DB_Adapter:
    __metaclass__ = abc.ABCMeta
 
    @abc.abstractmethod
    def search(self, query: str) -> list:
        """Search the database"""
        pass
 
    @abc.abstractmethod
    def add(self, title: str, content: str, tags: list) -> list:
        """Add an item to the database"""
        pass
 
 
class Output_Adapter:
    __metaclass__ = abc.ABCMeta
 
    @abc.abstractmethod
    def present(self, data: dict) -> str:
        """Present output"""
        pass
 
 
class Notes_TDB_Adapter(DB_Adapter):
    def __init__(self, path):
        self.tdb = TinyDB(path)
 
    def search(self, query) -> list:
        Note = Query()
        test_func = lambda s: query in s
        return self.tdb.search(Note.content.test(test_func) | Note.title.test(test_func) | Note.tags.any(query))
 
    def add(self, title, content, tags=[]):
        note = {
            "title": title,
            "content": content,
            "tags": tags
        }
        self.tdb.insert(note)
 
 
class Terminal_Output_Adapter(Output_Adapter):
 
    def present(self, data: list) -> str:
        outp = []
        for item in data:
            title = item.get("title")
            content = item.get("content")
            tags = item.get("tags")
            outp.append("Title: {}".format(title))
            outp.append("Content:")
            outp.append("\t{}".format(content))
            outp.append("Tags: {}".format(', '.join(tags)))
            outp.append("\n")
        return "\n".join(outp)
 
 
class Simple_JSON_Output_Adapter(Output_Adapter):
 
    def present(self, data: list) -> str:
        return json.dumps(data, indent=4, sort_keys=True)
 
 
class Notebook:
    def __init__(self, notes: DB_Adapter, output: Terminal_Output_Adapter):
        self.notes = notes
        self.output = output
 
    def search(self, query) -> str:
        return self.output.present(self.notes.search(query))
 
    def add(self, title, content, tags=[]):
        self.notes.add(title, content, tags)
 
 
if __name__ == '__main__':
    d = [
        {"title": "Books to Read", "content": "Gang of Four, Clean Architecture", "tags": ["books"]},
        {"title": "Hiking Trails", "content": "Coal Creek, Davidson Mesa", "tags": ["places"]},
        {"title": "Restaurants", "content": "Parma in Boulder", "tags": ["places", "food"]},
        {"title": "Cooking Class", "conent": "Class at Sur la Table, get free cast iron", "tags": ["food"]},
    ]
 
    TDB_JSON = "tdb.json"
    tdb = TinyDB(TDB_JSON)
    for item in d:
        tdb.insert(item)
 
    db_adapter = Notes_TDB_Adapter(TDB_JSON)
    output_adapter = Terminal_Output_Adapter()
    # output_adapter = Simple_JSON_Output_Adapter()
 
    notebook = Notebook(notes=db_adapter, output=output_adapter)
 
    # add a note
    notebook.add(title="History Books", content="The Color of Law, A People's History", tags=["books"])
 
    print(notebook.search("books"))
    print(notebook.search("food"))
