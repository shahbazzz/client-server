import rpyc
conn = rpyc.classic.connect("localhost")
print(type(conn.modules.sys))
conn.get_variable_on_daemon("x")