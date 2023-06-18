from reactpy import component, html, hooks
from reactpy.backend.fastapi import configure
from fastapi import FastAPI

@component
def Item(text):
  done, set_done = hooks.use_state(False)
  
  def handle_click(event):
    set_done(not done)

  if done:
    attr = { "style": { "color": "green", "text-decoration": "line-through" }, "on_click": handle_click }  
  else: 
    attr = { "style": { "color": "red" }, "on_click": handle_click }

  return html.li(attr, text)

@component
def Home():
  return html._(
    html.h1("Todo Tasks:"),
    html.ul(
      Item("Task 1"),
      Item("Task 1")
    )
  )

app = FastAPI()
configure(app, Home)