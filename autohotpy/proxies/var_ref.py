from autohotpy.proxies.ahk_object import AhkObject


class VarRef(AhkObject):
    @property
    def value(self):
        return self._ahk_instance.call_method(None, "_py_deref", (self,))

    @value.setter
    def value(self, new_value):
        self._ahk_instance.call_method(None, "_py_set_ref", (self, new_value))
