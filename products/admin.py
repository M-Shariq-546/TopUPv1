from import_export import resources, fields, widgets
from import_export.admin import ImportExportModelAdmin
from .models import Products
from django.contrib import admin

class ProductResource(resources.ModelResource):
    class Meta:
        model = Products
        fields = ('id', 'name', 'description', 'subcategory', 'price', 'quantity', 'image', 'created_at')
        export_order = ('id','name', 'description', 'subcategory', 'price', 'quantity', 'image', 'created_at')
        import_id_fields = ['id']  # This allows updating existing records by ID
        skip_unchanged = True  # Skip rows that haven't changed
        report_skipped = True  # Report skipped rows in the import preview

    def before_import_row(self, row, **kwargs):
        # If no ID is provided, we'll let Django generate one
        if not row.get('id'):
            row['id'] = None

@admin.register(Products)
class ProductAdmin(ImportExportModelAdmin):
    resource_class = ProductResource