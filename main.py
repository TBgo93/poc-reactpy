from reactpy import component, html, hooks, backend
from reactpy.backend.fastapi import configure, Options
from fastapi import FastAPI
from uuid import uuid4 as uuid


@component
def Wrapper(children):
  return html.div(
    { "style": 
      {
        "display": "grid", 
        "place-content": "center", 
        "gap": "18px"
      },
      "class": "page-wrapper"
    },
    children
  )

@component
def Item(id, title, done, delete_one, done_task):
  def handle_click(event):
    event["stop_propagation"] = True
    done_task(id, done)

  def handle_remove(event):
    delete_one(id)

  if done:
    style = { "text-decoration": "line-through" }
  else: 
    style = { "text-decoration": "none" } 

  return html.li(
    { "key": id },
    html.span({ "on_click": handle_click, "style": style }, title),
    html.code({ "on_click": handle_remove, "style": { "color": "red", "margin-left": "12px" } }, "x")
  )

@component
def ListOfTasks(tasks, delete_one, done_task):
  if tasks != []:
    list_item_elements = [Item(i["id"], i["title"], i["done"], delete_one, done_task) for i in tasks]
    return html.ul(list_item_elements)
  else:
    return html.span("Dont have a tasks, please add one")

@component
def AddTask(tasks, set_tasks):
  value, set_value = hooks.use_state("")
  is_empty_task, set_is_empty_task = hooks.use_state(False)
  def handle_change(event):
    set_value(event["target"]["value"])

  def handle_click(event):
    event["defaultPrevented"] = True
    if value != "":
      set_tasks([*tasks, {"id": uuid().hex, "title": value, "done": False }])
      set_value("")
      set_is_empty_task(False)
    else:
      set_is_empty_task(True)
      return
  
  if is_empty_task:
    display = { "display": "block", "font-size": "14px" }
  else:
    display = { "display": "none" }
  
  return html.div(
    { "style": { "display": "flex", "flex-direction": "column" ,"gap": "12px" } },
    html.div(
      { "style": { "display": "flex", "gap": "8px" } },
      html.input({ "placeholder": "Introduzca la task", "on_change": handle_change, "value": value }),
      html.button({ "on_click": handle_click }, "Agregar")
    ),
    html.code({ "style": display }, "Debe ingresar un texto para agregar a la lista")
  )

@component
def Home():
  tasks, set_tasks = hooks.use_state([])

  def delete_one(id):
    draft_tasks = tasks
    for x in tasks:
      if x["id"] == id:
        draft_tasks.remove(x)
    set_tasks([*draft_tasks])

  def done_task(id, done):
    draft_tasks = tasks
    for x in draft_tasks:
      if x["id"] == id:
        x["done"] = not done
    set_tasks([*draft_tasks])
  
  return Wrapper([
    html.h1("Todo list"),
    AddTask(tasks, set_tasks),
    ListOfTasks(tasks, delete_one, done_task)
  ])

app = FastAPI()

configure(app, Home, Options(head=({'tagName': 'title', 'children': ['TODO App']}, {'tagName': 'link', 'attributes': {'rel': 'icon', 'href': '/_reactpy/assets/reactpy-logo.ico', 'type': 'image/x-icon'}}, {'tagName': 'link', 'attributes': {'rel': 'stylesheet', 'href': 'https://cdn.simplecss.org/simple.min.css'}}), url_prefix='', cors=False))