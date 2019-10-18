def createInstance(module_name, class_name, cmd, op, params):
  module_meta = __import__(module_name, globals(), locals(), [class_name])
  class_meta = getattr(module_meta, class_name)
  obj = class_meta(cmd, op, params)
  return obj

obj = createInstance("operation", "SetVncPassword", cmd=123, op=123, params={})
print type(obj)
print obj.cmd
print obj.do