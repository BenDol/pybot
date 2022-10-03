# PyBot
![logo-128x128](https://github.com/BenDol/pybot/blob/master/media/logo-128x128.png)

## What is PyBot
PyBot is a Python scripting engine that provides a framework for building component based tasks with the following features: task dispatcher, component system, input controls, easy script configuration (via json), extendable script configuration, multithreading, and more!

## Purpose
The purpose of this project is to provide an easy to use task-based scripting engine that can be used as a foundation for simple or advanced tasks.

## Running the application
Install python 3.10.1+ from [python.org](https://www.python.org/)

Install requirements:
```
pip install .
```
Run with:
```
pybot-cli
```

## Building the application
Run `build.bat` the binary, scripts and settings are found in `/dist` directory

## How it works
PyBot loads using the [`settings.json`](https://github.com/BenDol/pybot/blob/master/settings.json) configurations. It will first attempt to "attach" to a given program if the bot tasks are dictatorial (configured from settings.json) programs can be added to [`/scripts/programs`](https://github.com/BenDol/pybot/tree/master/scripts/programs). Once attached it will then load any tasks specific to the program, which is also configurable. Next PyBot will load the components from [`/scripts/components`](https://github.com/BenDol/pybot/tree/master/scripts/components), once loaded it will load all scripts provided in [`/scripts`](https://github.com/BenDol/pybot/tree/master/scripts).

### Components
Components are isolated segments of logic that can be plugged into tasks using [`TaskComponent`](https://github.com/BenDol/pybot/blob/master/pybot/core/component.py#L22). The components are loaded from [`/scripts/components`](https://github.com/BenDol/pybot/tree/master/scripts/components) at startup. Here is an example of a component:
```python
class MouseMoveTaskComponent(TaskComponent):
  def __init__(self, config):
    super().__init__(config)
    self.position   = self.config.get("position")   or None
    self.speed      = self.config.get("speed")      or [25, 55]
    self.delay      = self.config.get("delay")      or None
    self.post_delay = self.config.get("post_delay") or [0, 0]

  def update(self, task):
    super().update(task)

    if self.position:
      self.program.mouse.navigate(xy=(self.position[0], self.position[1]), speed=self.speed, delay=self.delay)

    time.sleep(random.uniform(self.post_delay[0], self.post_delay[1]))

  def post_update(self, task):
    super().post_update(task)
```
This component will move the mouse based on the configuration it's provided.

### Tasks
Tasks are a multithreaded code execution that run on a delay.
```python
@task(delay=[1,4], silent=True)
def my_task(self, *args):
  return TaskHandler()
```
The above task will execute every rand(1, 4) seconds. We have marked it as silent so it doesn't print every execution to the console. The returned [`TaskHandler`](https://github.com/BenDol/pybot/blob/master/pybot/core/tasks.py#L92) is what allows us to fine-grain our task control. If `None` or `False` is returned the task will simply not execute.
```python
def can_start(task):
  return True
def started(task):
  print("task started")
def completed(task):
  print("task completed")
def failed(task, err):
  print("task failed")
return TaskHandler(can_start=can_start, started=started, completed=completed, failed=failed)
```
Configuring a task in our script configuration looks something like this:
```json
"tasks": {

  "my_task": {
    "enabled": true,
    "delay": [3, 6],
    "components": [{
      "name": "MouseMoveTaskComponent",
      "config": {
        "enabled": true,
        "position": [2300, 1140, 2320, 1164],
        "speed": [35, 65],
        "delay": [0.000001, 0.00002],
        "post_delay": [0.3, 0.5]
      }
    }]
  }
  
}
```
We can turn off our tasks by setting `"enabled": false` and you can see we have even overriden the `"delay"`. This task also has a component that will execute (in given order). There can be as many components as you like.

### Scripts
A script is a module that orcastrates tasks and components to accomplish a specific goal. The script must come with a `json` file of the same name (i.e. my_script.py must have my_script.json) which contains its default configurations, these configurations can be overriden inside the `settings.json "scripts":{}`. They are comprised of "tasks" which are configured scripts json configuration file. Tasks can then be comprised of components. The standard structure of a Script is like so:
```python
class MyScript(Script):
  def __init__(self, parent, config):
    super().__init__(parent, config, __name__)
    
   def load(self, conf):
    super().load(conf)

  def unload(self):
    super().unload()

  def start(self):
    super().start()
```
* `load` is called when the script is loaded at startup
* `unload` is called when the script is unloaded
* `start` is called when the program starts the script (generally at startup)

Scripts will often contain `@tasks` (see Tasks section above)

### Configuration
TODO

## License
MIT License

## Disclaimer
The sample scripts provided are made as test cases for automating some game tasks. This is strictly done as a way to improve PyBot. I am not responsible if this results in bans.
