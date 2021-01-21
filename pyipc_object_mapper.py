import tkinter
import sys

class RemoteTcl():
    def __init__(self,testset_ip, testset_port):
        self.testset = testset_ip
        self.port = testset_port
        # do import and all
        self.interp = tkinter.Tcl()
        print("###")

    def tcl_eval(self, tcl_code, *args, **kwargs):
        def_ret = dict()
        def_ret["exec_status"] = True
        def_ret["output"] = None
        def_ret["error"] = None
        orig_stdout = sys.stdout
        print(orig_stdout)
        f = open('out.txt', 'w')
        sys.stdout = f
        try:
            print("ddd")
            def_ret["output"] = self.interp.eval(tcl_code)
            def_ret["exec_status"] = True
        except Exception as e:
            def_ret["exec_status"] = False
            def_ret["error"] = str(e)
        sys.stdout = orig_stdout
        f.close()
        return def_ret
