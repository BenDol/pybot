class Component(object):
  def __init__(self, config):
    self.config = config
    self.enabled = config["enabled"]
    self.program = None

  def load(self, owner):
    if hasattr(owner, "program"):
      self.program = owner.program
    else:
      print(" ERROR: No program object found in Component origin!")

  def unload(self):
    pass

  def update(self):
    pass

  def post_update(self):
    pass

class TaskComponent(Component):
  def __init__(self, config):
    super().__init__(config)
    self.parallel = config.get("parallel") or False

  def load(self, owner):
    super().load(owner)

  def unload(self):
    super().unload()

  def update(self, task):
    super().update()

  def post_update(self, task):
    super().post_update()
