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
        self.books = {}

        self.periodic_task()
    
    def new_book(self):
        if self.couch is None:
            return dict()
        book_id = self.time_str + " " + ''.join(random.choices(string.ascii_lowercase, k=3))
        book = CBBook(self, book_id=book_id)
        self.books[book_id] = book
        return book
    
    def get_list(self):
        pass

    def periodic_task(self):
        if self.couch is None:
            return
        t = threading.Timer(self.SAVE_PERIOD, self.periodic_task)
        t.daemon = True
        t.start()
        try:
            self.save()
        except:
            pass

    def save(self):
        if self.couch is None:
            return
        for book_id, book in self.books.items():
            if not book.write_flag:
                continue
            self.db[book_id] = book.content
            self.db.save(self.db[book_id])
            book.write_flag = False

    @property
    def time_str(self):
        return datetime.datetime.now().strftime("%y-%m-%d %H-%M-%S")
    
    @property
    def iso_time_str(self):
        return datetime.datetime.now().isoformat()

class CBBook:
    def __init__(self, cbed, book_id):
        self.cbed = cbed
        self.book_id = book_id
        self.stopwatch_dict = {"startup": time.time()}
        self.log_dict = {}
        self.write_flag = False
        self.content = {"msg": [], "log": [], "setting": {}, "created": self.cbed.iso_time_str, "last_updated": self.cbed.iso_time_str, "result": {}}

    def __call__(self, *args):
        self.message(" ".join([f"{x}" for x in args]))

    def message(self, msg):
        time_stamped_msg = self.cbed.time_str +": "+ msg
        self.content["msg"].append(time_stamped_msg)
        self.write_flag = True
        self.content["last_updated"] = self.cbed.iso_time_str
        print(time_stamped_msg)
    
    def start_stopwatch(self, watch_name):
        self.stopwatch_dict[watch_name] = time.time()

    def record_stopwatch(self, watch_name="startup", msg=None):
        if watch_name in self.stopwatch_dict:
            dt = time.time() - self.stopwatch_dict[watch_name]
            self.message(f"{watch_name} -> {dt} {f'({msg})' if msg is not None else ''}")
    
    def set(self, setting_dict):
        self.content["setting"].update(self.sanitize(setting_dict))
        self.write_flag = True
        self.content["last_updated"] = self.cbed.iso_time_str

    def __setitem__(self, key, value):
        self.content["setting"][key] = self.sanitize(value)
        self.write_flag = True
        self.content["last_updated"] = self.cbed.iso_time_str

    def __getitem__(self, key):
        if key in self.content["setting"]:
            return self.content["setting"][key]
        return None

    def log(self, log_dict):
        log_dict = self.sanitize(log_dict)
        log_dict["_time"] = self.cbed.iso_time_str
        self.content["log"].append(log_dict)
        print(", ".join([f"{key}:{value}" for key, value in log_dict.items()]))
        self.content["last_updated"] = self.cbed.iso_time_str
        self.write_flag = True
        
    
    def result(self, result_dict):
        result_dict = self.sanitize(result_dict)
        result_dict["_time"] = self.cbed.iso_time_str
        self.content["result"].update(result_dict)
        self.content["last_updated"] = self.cbed.iso_time_str
        self.write_flag = True
        

    def save(self):
        self.cbed.save()

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
