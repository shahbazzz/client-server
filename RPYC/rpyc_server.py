import sys
import rpyc
import tkinter
from rpyc.utils.server import ThreadedServer

# or ForkingServer
PORT = 5050
archive = dict()
tcl_archive = dict()

class IPC(rpyc.Service):
    def exposed_redirect(self, stdout):
        sys.stdout = stdout
    def exposed_restore(self):
        sys.stdout = sys.__stdout__

    def exposed_set_variable_on_daemon(self, key, value, *args, **kwargs):
        global archive
        archive[key] = value
        print(f"{PORT}> client setting key:{key}, value:{value}")
        if key in archive and archive[key] == value:
            return True
        else:
            return False

    def exposed_get_variable_on_daemon(self, key, *args, **kwargs):
        global archive
        print(f"{PORT}> client getting key: {key}")
        if key in archive:
            print(f"value: {archive[key]}")
            return archive[key]
        else:
            print("not found.")
            return None

    def exposed_del_variable_on_daemon(self, key, *args, **kwargs):
        global archive
        print(f"{PORT}> client deleting key: {key}")
        if key in archive:
            print(f"value: {archive[key]}")
            del archive[key]
            return True
        else:
            print("not found.")
            return None

    def exposed_run_tcl_cmd(self, key, cmd, r_out, *args, **kwargs):
        global tcl_archive
        if key in tcl_archive:
            sys.stdout = r_out
            ret = tcl_archive[key].eval(cmd)
            sys.stdout = sys.__stdout__
            print(f"TCL INTERPRETER FOUND. {cmd}")

            return ret
        else:
            print("TCL INTERPRETER NOT FOUND!")
            return None

    def exposed_new_tcl_interpreter(self, key, *args, **kwargs):
        global tcl_archive
        print(f"{PORT}> client adding tcl interpreter: {key}")
        interpreter = tkinter.Tcl()
        #if key in tcl_archive:
        #    try:
        #        del tcl_archive[key]
        #    except Exception as e:
        #       print(f"Exception: {e}")
        tcl_archive[key] = interpreter
        print(f"Tcl intrep: {interpreter} {type(interpreter)}")
        x=interpreter.eval("puts \"===\"")
        print(type(x))
        return interpreter

    def exposed_get_tcl_interpreter(self, key, *args, **kwargs):
        global tcl_archive
        print("-----------------")
        print(tcl_archive)
        print("-----------------")
        print(f"{PORT}> client getting tcl interpreter: {key}")
        if key in tcl_archive:
            print(f"Tcl intrep: {tcl_archive[key]}")
        else:
            print(f"not available")
            return None

    def exposed_del_tcl_interpreter(self, key, *args, **kwargs):
        global archive
        print(f"{PORT}> client deleting tcl interpreter: {key}")
        if key in tcl_archive:
            print(f"interpreter: {tcl_archive[key]}")
            return True
        else:
            print(f"not available")
            return False


server = ThreadedServer(IPC, port = PORT)
print(f"Server running on {server.port} >>>\n")
server.start()