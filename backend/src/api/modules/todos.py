import json
import logging
from typing import Any
from ...services import TodoService
from ...utils.response import format_response

logger = logging.getLogger(__name__)

def setup_todos_api(window, container):
    todo_service = container.resolve(TodoService)

    def get_todos(e: Any):
        try:
            data = todo_service.get_all()
            return json.dumps(format_response(True, data))
        except Exception as ex:
            return json.dumps(format_response(False, error=str(ex)))

    def create_todo(e: Any):
        try:
            task = e.get_string()
            data = todo_service.create(task)
            return json.dumps(format_response(True, data))
        except Exception as ex:
            return json.dumps(format_response(False, error=str(ex)))

    def toggle_todo(e: Any):
        try:
            todo_id = e.get_string()
            success = todo_service.toggle(todo_id)
            return json.dumps(format_response(success))
        except Exception as ex:
            return json.dumps(format_response(False, error=str(ex)))

    def delete_todo(e: Any):
        try:
            todo_id = e.get_string()
            success = todo_service.delete(todo_id)
            return json.dumps(format_response(success))
        except Exception as ex:
            return json.dumps(format_response(False, error=str(ex)))

    def clear_completed_todos(e: Any):
        try:
            count = todo_service.clear_completed()
            return json.dumps(format_response(True, count))
        except Exception as ex:
            return json.dumps(format_response(False, error=str(ex)))

    window.bind("get_todos", get_todos)
    window.bind("create_todo", create_todo)
    window.bind("toggle_todo", toggle_todo)
    window.bind("delete_todo", delete_todo)
    window.bind("clear_completed_todos", clear_completed_todos)
