import json
import jsonpickle
from json import JSONEncoder
from .utils import timing

class Things:
    def __init__(self, name, count):
        self.name = name
        #self.template = template
        self.count = count        

    def increase_count(self, delta_count):
        self.count += delta_count

class Sublevel:
    def __init__(self, name):
        self.name = name
        self.things = {}
        self.sublevels = {}

    def add_things(self, things):
        self.things[things.name] = things

    def add_sublevel(self, name):
        self.sublevels[name] = Sublevel(name)

    def delete_things(self, name):
        del self.things[name]
    
    def delete_sublevel(self, name):
        del self.sublevels[name]

    def get_sublevel_names(self):
        return list(self.sublevels.keys())

    def get_things_names(self):
        return list(self.things.keys())

    def print_tree(self, indent=0):
        for name, t in self.things.items():
            print("  " * indent + f"- {name} ({t.__dict__})")
        for name, sub in self.sublevels.items():
            print("  " * indent + f"- {name}")
            sub.print_tree(indent=indent+1)

class Hierarchy(Sublevel):
    def __init__(self):
        self.things = {}
        self.sublevels = {}
        self.name = "top"

    def add_sublevel_to_path(self, location_path, name):
        current = self
        for p in location_path:
            current = current.sublevels[p]

        current.add_sublevel(name)

    def add_things_to_path(self, location_path, things):
        current = self
        for p in location_path:
            current = current.sublevels[p]

        current.add_things(things)

    def delete_things_from_path(self, location_path, name):
        current = self
        for p in location_path:
            current = current.sublevels[p]

        current.delete_things(name)

    def delete_sublevel_from_path(self, location_path, name):
        current = self
        for p in location_path:
            current = current.sublevels[p]

        current.delete_sublevel(name)

    def get_sublevel_names_from_path(self, location_path):
        current = self
        for p in location_path:
            current = current.sublevels[p]

        return current.get_sublevel_names()

    def get_things_names_from_path(self, location_path):
        current = self
        for p in location_path:
            current = current.sublevels[p]

        return current.get_things_names()

    def print_tree(self, indent=0):
        print("Top level: ")
        super().print_tree()

    @timing
    def save(self, save_file):
        hierarchyJSON = jsonpickle.encode(h, unpicklable=True)
        out = json.dumps(hierarchyJSON, indent=4)

        with open(save_file, 'w') as f:
            f.write(out)


@timing
def load_hierarchy_from_file(file):
    with open(file, 'r') as f:
        h = jsonpickle.decode(json.loads(f.read()))

    return h

if __name__ == "__main__":
    h = Hierarchy()
    h.add_sublevel("Audio")
    h.add_sublevel("Video")
    h.add_sublevel("Licht")
    h.add_sublevel("Rigging")
    h.add_sublevel("Allgemein")
    h.add_sublevel("Sonstiges")

    h.add_things(Things("Stromkabel 30m 16A", 3))
    h.add_sublevel_to_path(["Video"], "VGA Kabel Box")
    h.add_things_to_path(["Video", "VGA Kabel Box"], Things("VGA Kabel 3m", 10))
    h.add_things_to_path(["Video", "VGA Kabel Box"], Things("VGA Kabel 5m", 5))
    h.add_things_to_path(["Video", "VGA Kabel Box"], Things("VGA Kabel 1m", 13))

    #h.print_tree()
    h.save("backup.json")

    del h

    h = load_hierarchy_from_file("backup.json")
    h.print_tree()