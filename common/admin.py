from django.contrib import admin


class XsmModelAdmin(admin.ModelAdmin):
    # A handy constant for the name of the alternate database.
    using = 'xsm'

    def save_form(self, request, form, change):
        print('save_form')
        return super().save_form(request, form, change)

    def save_model(self, request, obj, form, change):
        # Tell Django to save objects to the 'other' database.
        print('save_model')
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        # Tell Django to delete objects from the 'other' database
        obj.delete(using=self.using)

    def get_queryset(self, request):
        # Tell Django to look for objects on the 'other' database.
        return super().get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super().formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super().formfield_for_manytomany(db_field, request, using=self.using, **kwargs)

class BaseModelAdmin(admin.ModelAdmin):

    ordering = ('-created',)