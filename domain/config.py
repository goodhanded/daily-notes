import configparser

class Config:
  def __init__(self):
    self.config = configparser.ConfigParser()
    self.config.read('config.ini')

  def get(self, section, key):
    return self.config[section][key]