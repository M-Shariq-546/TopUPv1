from django.contrib import admin
from import_export import resources, fields, widgets
from import_export.admin import ImportExportModelAdmin
from .models import Category

class CategoryResource(resources.ModelResource):
    parent_category = fields.Field(
        column_name='parent_category',
        attribute='parent_category',
        widget=widgets.ForeignKeyWidget(Category, 'name')
    )
    
    class Meta:
        model = Category
        fields = ('id', 'name', 'description', 'image', 'parent_category')
        export_order = ('id', 'name', 'description', 'image', 'parent_category')
        import_id_fields = ['id']  # This allows updating existing records by ID
        skip_unchanged = True  # Skip rows that haven't changed
        report_skipped = True  # Report skipped rows in the import preview

    def before_import_row(self, row, **kwargs):
        # If no ID is provided, we'll let Django generate one
        if not row.get('id'):
            row['id'] = None

@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    resource_class = CategoryResource
    list_display = ('name', 'description', 'image', 'parent_category')
    search_fields = ('name',)
