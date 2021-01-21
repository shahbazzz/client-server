import sys
import rpyc
import time
PORT = 5050
import tkinter

conn = rpyc.connect("127.0.0.1", port=PORT,  config={"allow_public_attrs":True})
#snd = conn.root.set_variable_on_daemon("x","7")
#print(snd)
snd = conn.root.get_variable_on_daemon("x")
print(snd)
try:
    snd = conn.root.new_tcl_interpreter("x")
    print(snd)
    time.sleep(10)
    print(type(snd))
    snd.eval("puts \"-----\"")
    snd = conn.root.del_tcl_interpreter("x")
except:
    pass
exit()
print(type(snd))
snd = conn.root.run_tcl_cmd("x", "puts \"------\"", sys.stdout)
exit()
snd = conn.root.del_variable_on_daemon("x")
print(snd)
snd = conn.root.get_variable_on_daemon("x")
print(snd)

snd.eval("puts \"=====\"")


conn.root.exposed_redirect(sys.stdout)
snd = conn.root.run_tcl_cmd("x", "puts \"------\"", sys.stdout)
conn.root.restore()
print(snd)