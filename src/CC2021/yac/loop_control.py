class LoopControl():
  def __init__(self):
    self.label = ''
  
  def set_next_label(self, label):
    self.label = label
  
  def get_next_label(self):
    return self.label