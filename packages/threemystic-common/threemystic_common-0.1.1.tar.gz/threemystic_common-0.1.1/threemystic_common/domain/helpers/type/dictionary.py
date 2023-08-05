from threemystic_common.base_class.base_common import base


class helper_type_dictionary(base): 
  """This is a set of library wrappers to help around expending dictionary libary"""

  def __init__(self, *args, **kwargs) -> None:
    super().__init__(logger_name= f"helper_type_dictionary", *args, **kwargs)
  
  def _merge_dictionary_find_main_dictionary_index(self, dicts, *args, **kwargs):
    if dicts[0] is not None:
      return 0

    for idx, item in enumerate(dicts[1:]):
      if item is None:
        continue
      
      return idx + 1
    
    return -1

  def merge_dictionary(self, dict1, dict2 = None, replace_on_merge = False, custom_handlers = {}, unique_list = False, update_first_dictionary = True):
    if dict1 is None and dict2 is None:
      return None
    if dict1 is None and dict2 is not None:
      return dict2

    if self._main_reference.helper_type().general().is_type(dict1, list):
      main_dict_index = self._merge_dictionary_find_main_dictionary_index(dicts= dict1)
      if main_dict_index < 0:
        return None
      
      return_dict = dict1[main_dict_index] if update_first_dictionary else {}.update(dict1[main_dict_index])      
      if (main_dict_index + 1) == len(dict1):
        return return_dict

      for dict_item in dict1[main_dict_index:]:
        self.merge_dictionary(dict1= return_dict, dict2=dict_item,)
      return return_dict

    if dict2 is None:
      return dict1
    
    update_dictionary = dict1 if update_first_dictionary else {}.update(dict1)
    if replace_on_merge:
      update_dictionary.update(dict2)
      return update_dictionary

    dict2_copy = self._main_reference.helper_type().general().copy_object(object_copy= dict2)

    for key, item in update_dictionary.items():
      if self._main_reference.helper_type().general().is_type(item, dict):
        if key in dict2_copy:
          self.merge_dictionary(item, dict2_copy[key])
          dict2_copy.pop(key, None)
        continue
      if self._main_reference.helper_type().general().is_type(item, list):
        if key in dict2_copy:
          item += dict2_copy[key]
          if unique_list:
            item = self._main_reference.helper_type().list().unique_list(item)
          dict2_copy.pop(key, None)
          
        continue
      
    update_dictionary.update(dict2_copy)
    
    return update_dictionary