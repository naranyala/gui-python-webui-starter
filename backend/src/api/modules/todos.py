import json
import logging
from typing import Any
from ...utils.response import format_response, api_handler

logger = logging.getLogger(__name__)

def setup_todos_api(window, container):
    todo_service = container.resolve("todo_service")

    @api_handler
    def get_todos(e: Any):
        return todo_service.get_all()

    @api_handler
    def create_todo(e: Any):
        task = e.get_string()
        return todo_service.create(task)

    @api_handler
    def toggle_todo(e: Any):
        todo_id = e.get_string()
        return todo_service.toggle(todo_id)

    @api_handler
    def delete_todo(e: Any):
        todo_id = e.get_string()
        return todo_service.delete(todo_id)

    @api_handler
    def clear_completed_todos(e: Any):
        return todo_service.clear_completed()

    window.bind("get_todos", get_todos)
    window.bind("create_todo", create_todo)
    window.bind("toggle_todo", toggle_todo)
    window.bind("delete_todo", delete_todo)
    window.bind("clear_completed_todos", clear_completed_todos)
