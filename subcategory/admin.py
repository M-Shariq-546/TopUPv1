from django.contrib import admin
from import_export import resources, fields, widgets
from import_export.admin import ImportExportModelAdmin
from .models import SubCategory

class SubcategoryResource(resources.ModelResource):
    class Meta:
        model = SubCategory
        fields = ('id', 'name', 'description', 'category','image', 'created_at')
        export_order = ('id','name', 'description', 'category','image', 'created_at')
        import_id_fields = ['id']  # This allows updating existing records by ID
        skip_unchanged = True  # Skip rows that haven't changed
        report_skipped = True  # Report skipped rows in the import preview

    def before_import_row(self, row, **kwargs):
        # If no ID is provided, we'll let Django generate one
        if not row.get('id'):
            row['id'] = None

@admin.register(SubCategory)
class SubcategoryAdmin(ImportExportModelAdmin):
    list_display = ('id', 'name')
    resource_class = SubcategoryResource