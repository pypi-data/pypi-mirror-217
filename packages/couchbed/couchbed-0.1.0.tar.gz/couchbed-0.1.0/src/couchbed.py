import random, string, time, os, threading, datetime, ast
import couchdb

class CouchBed:
    SAVE_PERIOD = 5.0 # (s)
    def __init__(self, db_name, uri=None, environ_var="PYTHON_COUCHBED"):
        if uri is None:
            uri = os.environ.get(environ_var, None)
        self.couch = None
        if uri is None:
            return
        self.couch = couchdb.Server(uri)
        if db_name in self.couch:
            self.db = self.couch[db_name]
        else:
            self.db = self.couch.create(db_name)
        self.db_name = db_name
        self.doc_id = self.time_str + " " + ''.join(random.choices(string.ascii_lowercase, k=3))
        self.stopwatch_dict = {"startup": time.time()}
        self.log_dict = {}
        self.write_flag = False
        self.doc = {"msg": [], "log": [], "setting": {}}
        self.periodic_task()
            
    
    def __call__(self, *args):
        if self.couch is None:
            return
        self.message(" ".join([f"{x}" for x in args]))

    def message(self, msg):
        if self.couch is None:
            return
        time_stamped_msg = self.time_str +": "+ msg
        self.doc["msg"].append(time_stamped_msg)
        self.write_flag = True
        print(time_stamped_msg)
    
    def start_stopwatch(self, watch_name):
        if self.couch is None:
            return
        self.stopwatch_dict[watch_name] = time.time()

    def record_stopwatch(self, watch_name="startup", msg=None):
        if self.couch is None:
            return
        if watch_name in self.stopwatch_dict:
            dt = time.time() - self.stopwatch_dict[watch_name]
            self.message(f"{watch_name} -> {dt} {f'({msg})' if msg is not None else ''}")
    
    def set(self, setting_dict):
        if self.couch is None:
            return
        self.doc["setting"].update(self.sanitize(setting_dict))
        self.write_flag = True

    def __setitem__(self, key, value):
        if self.couch is None:
            return
        self.doc["setting"][key] = self.sanitize(value)
        self.write_flag = True

    def __getitem__(self, key):
        if self.couch is None:
            return
        if key in self.doc["setting"]:
            return self.doc["setting"][key]
        return None

    def log(self, log_dict):
        if self.couch is None:
            return
        log_dict = self.sanitize(log_dict)
        log_dict["_time"] = self.time_str
        self.doc["log"].append(log_dict)
        print(", ".join([f"{key}:{value}" for key, value in log_dict.items()]))
        self.write_flag = True

    def periodic_task(self):
        if self.couch is None:
            return
        t = threading.Timer(self.SAVE_PERIOD, self.periodic_task)
        t.daemon = True
        t.start()
        if self.write_flag:
            try:
                self.save()
            except:
                pass
    
    def sanitize(self, value):
        if isinstance(value, (str, float, int)):
            return value
        elif isinstance(value, dict):
            result_dict = {}
            for k, v in value.items():
                result_dict[k] = self.sanitize(v)
            return result_dict
        else:
            return ast.literal_eval(f"{value}")
            

    def save(self):
        if self.couch is None:
            return
        if not self.write_flag:
            pass
        if isinstance(self.doc, dict):
            self.db[self.doc_id] = self.doc
            self.doc = self.db[self.doc_id]
        self.db.save(self.doc)
        self.write_flag = False

    @property
    def time_str(self):
        return datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")