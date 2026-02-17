from django.urls import path
from .views import (
    delete_project_record,
    export_project_txt,
    project_input_view,
    project_records_view,
    project_results_view,
)

urlpatterns = [
    path("", project_input_view, name="project_input"),
    path("records/", project_records_view, name="project_records"),
    path("records/<int:project_id>/", project_results_view, name="project_results"),
    path("records/<int:project_id>/delete/", delete_project_record, name="delete_project_record"),
    path("export/<int:project_id>/txt/", export_project_txt, name="export_project_txt"),
]
