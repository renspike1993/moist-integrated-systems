class AppRouter:
    """
    Routes database operations for registrar and library apps.
    """

    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'registrar':
            return 'default'
        elif model._meta.app_label == 'library':
            return 'library_db'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'registrar':
            return 'default'
        elif model._meta.app_label == 'library':
            return 'library_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        # Allow relations within the same app
        if obj1._meta.app_label == obj2._meta.app_label:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'registrar':
            return db == 'default'
        elif app_label == 'library':
            return db == 'library_db'
        return None
