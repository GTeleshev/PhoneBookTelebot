import json
import csv

from ConnectDb import ConnectDb


class Notes:
    def __init__(self):
        self.connect = ConnectDb()
        self.all_notes = self.connect.all_data_dict

    def add_note(self, data):
        self.all_notes[max([int(item) for item in self.all_notes.keys()]) + 1 if self.all_notes != {} else 0] = {
            'lastname': data[0],
            'firstname': data[1],
            'phone': data[2],
            'description': data[3]
        }

    def import_notes(self, name_file, type='json'):
        if type not in ["csv", "json", "sql"]:
            return False
        if type == "json":
            with open(name_file, "r", encoding="utf-8") as f:
                for key, value in json.load(f).items():
                    self.all_notes[
                        max([int(item) for item in self.all_notes.keys()]) + 1 if self.all_notes != {} else 0] = {
                        'lastname': value["lastname"],
                        'firstname': value["firstname"],
                        'phone': value["phone"],
                        'description': value["description"]
                    }
        if type == "csv":
            with open(name_file, newline="") as f:
                reader = csv.reader(f)
                for row in reader:
                    self.all_notes[
                        max([int(item) for item in self.all_notes.keys()]) + 1 if self.all_notes != {} else 0] = {
                        'lastname': row[0],
                        'firstname': row[1],
                        'phone': row[2],
                        'description': row[3]
                    }
        if type == "sql":
            connect = ConnectDb(name_file)
            all_notes = connect.all_data_dict
            for key, value in all_notes.items():
                self.all_notes[
                    max([int(item) for item in self.all_notes.keys()]) + 1 if self.all_notes != {} else 0] = {
                    'lastname': value["lastname"],
                    'firstname': value["firstname"],
                    'phone': value["phone"],
                    'description': value["description"]
                }

    def export_json(self, file, type='json'):
        with open(f"{file}.json", "w", encoding="utf-8") as f:
            json.dump(self.all_notes, f, indent=4, ensure_ascii=False)

    def get_all(self):
        return self.all_notes

    def delete_by_id(self, id):
        del self.all_notes[int(id)]

    def change_by_id(self, id, data):
        if id in self.all_notes.keys():
            self.all_notes[id] = {
                'lastname': data[0],
                'firstname': data[1],
                'phone': data[2],
                'description': data[3]
            }
            return True
        else:
            return False

    def clear_all(self):
        self.all_notes = {}
        self.connect.clear_db()

    def end(self):
        self.connect.finish(self.all_notes)

    def search(self, lastname):
        res = []
        for key, value in self.all_notes.items():
            if value['lastname'].lower() == lastname.lower():
                temp = {}
                temp[key] = value
                res.append(temp)
        return res

    def export_notes(self, name_file, type="json"):
        if type not in ["csv", "json"]:
            return False
        if type == "json":
            with open(f"{name_file}.json", "w", encoding="utf-8") as f:
                json.dump(self.all_notes, f, indent=4, ensure_ascii=False)
        if type == "csv":
            with open(f"{name_file}.csv", "w", encoding="utf-8") as f:
                writer = csv.writer(f)
                for key, value in self.all_notes.items():
                    writer.writerow([value["lastname"], value["firstname"], value["phone"], value["description"]])
