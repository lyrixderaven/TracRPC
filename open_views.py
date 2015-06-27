class OpenViews():
    cache = []

    @classmethod
    def get(cls, view):
        for view_dict in cls.cache:
            if view_dict['id'] == view.id():
                return view_dict

    @classmethod
    def set(cls, view):
        cls.cache.append({'id': view.id()})

    @classmethod
    def exists(cls, view):
        return True if cls.get(view) else False

    @classmethod
    def remove(cls, view_to_remove):
        view_dict = cls.get(view_to_remove)
        if view_dict:
            cls.cache.remove(view_dict)
