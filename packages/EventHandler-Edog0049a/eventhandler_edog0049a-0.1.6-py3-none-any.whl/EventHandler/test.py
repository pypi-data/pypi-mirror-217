from EventHandler import EventHandler

event = EventHandler()
event.on("test", lambda sender, obj: print(obj))
event.emit("","test", "Hello World")

